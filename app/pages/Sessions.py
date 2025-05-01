# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from style import custom_sidebar_css, custom_metric_card
from plotly.subplots import make_subplots

#page setup
st.set_page_config(
    page_title="Sessions Overview",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

#inject css to background and sidebar 
custom_sidebar_css()

#load and prepare data 
@st.cache_data
def get_master_data():
    path = Path(__file__).resolve().parent.parent  #path of app's script
    df = pd.read_csv(path / 'master.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['DistanceToPin_Yrds'] = df['DistanceToPin_Yrds'].apply(lambda x: float(x.split(' ')[0]))
    return df

data = get_master_data()

#set sidebar up
with st.sidebar:
    st.title('Golf Simulation Statistics')
    
    #filter for date change
    min_date = data['Date'].min().date()
    max_date = data['Date'].max().date()
    date_range = st.date_input('Date Range', [min_date, max_date])
    if len(date_range) != 2:
        st.stop()
    
    #club list for  filter 
    club_list = ['All'] + sorted(list(set(data['Club'])))
    
    #select metrics 
    not_metrics = ['Date', 'Month', 'Unnamed: 0', 'Club', 'Decent']
    metric_opts = ['All'] + [i for i in set(data.columns) if i not in not_metrics]
    

#MAIN CONTENT
tab1, tab2, tab3 = st.tabs(["Performance", "Angle of Attack", "Smash Factor"])

with tab1:
    st.markdown("## 🏌️‍♂️Performance Metrics")
    col_filters = st.columns(2)
    with col_filters[0]:
        clubs = ['All'] + sorted(data['Club'].unique())
        selected_club = st.selectbox("Filter by Club", clubs, index=0, key='club_filter_tab1')

    with col_filters[1]:
        all_metrics = [i for i in data.columns if i not in not_metrics]
        selected_metric = st.selectbox("Select Metric", all_metrics, key='selected_metric_inline')

    #filter data
    filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]
    if selected_club != 'All':
        filtered = filtered[filtered['Club'] == selected_club]
  
    #show metric cards
    cols = st.columns((1, 4), gap='small')
    with cols[0]:
        min = filtered[selected_metric].min()
        avg = filtered[selected_metric].mean()
        max = filtered[selected_metric].max()
        std = filtered[selected_metric].std()
        count = filtered[selected_metric].count()
        if not pd.isna(avg):
            custom_metric_card(label="Minimum", value=f"{min:.1f}")
            custom_metric_card(label="Average", value=f"{avg:.1f}")
            custom_metric_card(label="Maximum", value=f"{max:.1f}")
            custom_metric_card(label="Standard Deviation", value=f"{std:.1f}")
            st.caption(f"Total Shots: {count}")

    with cols[1]:
        st.markdown("### Average Distance to Pin Over Time by Club")
        #multiselection for clubs 
        club_multiselect = st.multiselect(
            "Filter clubs", 
            sorted(filtered['Club'].unique()), 
            default=sorted(filtered['Club'].unique()),
            key="performance_chart_club_filter"
        )

        filtered_chart = filtered[filtered['Club'].isin(club_multiselect)]
        grouped = (
            filtered_chart
            .groupby(['Date', 'Club'])['DistanceToPin_Yrds']
            .mean()
            .reset_index()
        )

        fig = px.scatter(
            grouped,
            x='Date',
            y='DistanceToPin_Yrds',
            color='Club',
            trendline='ols',
            labels={'DistanceToPin_Yrds': 'Avg Distance to Pin (Yards)'},
            title=''
        )
        fig.update_yaxes(rangemode='tozero')
        st.plotly_chart(fig, use_container_width=True)



with tab2:
    #st.markdown("## Angle of Attacks vs. Club Type")

    col_filters2 = st.columns(2)
    # with col_filters2[0]:
    #     # Club type selector
    #     club_opts = filtered['Club'].unique()
    #     selected_club = st.selectbox("Select Club Type", options=club_opts)

    #filter data
    filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

    cols = st.columns((4, 4), gap='medium')
    with cols[0]:
        #multiselection for clubs 
        club_multiselect2 = st.multiselect(
            "Filter clubs", 
            sorted(filtered['Club'].unique()), 
            default=sorted(filtered['Club'].unique()),
            key="AoA_chart_club_filter"
        )

        # Filter the data based on selection
        filtered_chart2 = filtered[filtered['Club'].isin(club_multiselect2)]

        #create secondary y-axis
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])

        # plot a scatter chart by specifying the x and y values
        # Use add_trace function to specify secondary_y axes.
        fig4.add_trace(
            go.Scatter(x=filtered_chart2['AoA'], y=filtered_chart2['Carry'], name="Angle of Attack", mode = 'markers', marker=dict(color='blue')),
            secondary_y=False)

        # Use add_trace function and specify secondary_y axes = True.
        fig4.add_trace(
            go.Scatter(x=filtered_chart2['AoA'], y=filtered_chart2['PeakHeight'], name="Peak Height", mode= 'markers', marker=dict(color='red')),
            secondary_y=True)

        # Adding title text to the figure
        # fig4.update_layout(
        #     title_text="Multiple Y Axis in Plotly"
        # )

        # Naming x-axis
        fig4.update_xaxes(title_text="Angle of Attack")

        # Naming y-axes
        fig4.update_yaxes(title_text="<b>Carry Distance</b>", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Peak Height</b> ", secondary_y=True)
        st.plotly_chart(fig4, use_container_width=True)

    #group by club, get mean AoA and count
        grouped1 = (
            filtered
            .groupby('Club', observed=True)
            .agg(AoA=('AoA', 'mean'), Count=('AoA', 'count'))
            .reset_index()
        )
        st.markdown("Angle of Attacks vs. Club Type")
        # Create bubble chart
        fig2 = px.scatter(
            grouped1,
            x='Club',
            y='AoA',
            size='Count',#number of shots            
            color='Club',
            labels={'AoA': 'Mean Angle of Attack', 'Count': 'Shot Count'},
            title='',
            size_max=40            
        )

        fig2.update_yaxes(range=[filtered['AoA'].min() - 1, filtered['AoA'].max() + 1])
        st.plotly_chart(fig2, use_container_width=True)
    
    with cols[1]:
        st.markdown("Angle of Attacks vs. Carry Distance")
        
        # Create bins 
        bin_edges = [0, 50, 75, 100, 125, 150, 175, 200,225]
        bin_labels = ['0–50', '50–75', '75–100', '100-125', '125-150', '150–175', '175–200', '200-225']
        filtered['CarryBin'] = pd.cut(filtered['Carry'], bins=bin_edges, labels=bin_labels, right=False)
        binned = filtered.groupby('CarryBin', observed=True).agg({'AoA': 'mean'}).reset_index()

        fig3 = px.bar(
        binned,
        x='CarryBin',
        y='AoA',
        #barmode= 'group',
        color='CarryBin',
        labels={'CarryBin': 'Carry Distance (Yard Bins)', 'AoA': 'Average AoA'},
        title=''
    )
        fig3.update_yaxes(range = [filtered['AoA'].min() - 1,filtered['AoA'].max() + 1])
        st.plotly_chart(fig3, use_container_width=True)

        





 