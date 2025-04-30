# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
import plotly.express as px
from style import custom_sidebar_css, custom_metric_card

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
    
    #club type filter 
    club_list = ['All'] + sorted(list(set(data['Club'])))
    #selected_club = st.selectbox('Select Club', club_list, index=0)
    
    #select metrics 
    not_metrics = ['Date', 'Month', 'Unnamed: 0', 'Club', 'Decent']
    #metrics = ['Carry', 'Path']
    metric_opts = ['All'] + [i for i in set(data.columns) if i not in not_metrics]
    #selected_metric = st.selectbox('Primary Metric', metric_opts,index=0)  #default to All
    
   
#filter data 
#filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

#MAIN CONTENT
tab1, tab2 = st.tabs(["Performance", "Tab 2"])

with tab1:
    st.markdown("## 🏌️‍♂️Performance Metrics")
    col_filters = st.columns(4)
    with col_filters[0]:
        clubs = ['All'] + sorted(data['Club'].unique())
        selected_club = st.selectbox("Filter by Club", clubs, index=0, key='club_filter_inline')
    with col_filters[1]:
        selected_avg_metric = st.selectbox("Select Average Metric", [col for col in data.columns if col not in not_metrics], key='avg_metric_inline')
    with col_filters[2]:
        selected_max_metric = st.selectbox("Select Maximum Metric", [col for col in data.columns if col not in not_metrics], key='max_metric_inline')
    with col_filters[3]:
        selected_min_metric = st.selectbox("Select Minimum Metric", [col for col in data.columns if col not in not_metrics], key='min_metric_inline')

    #filter data
    filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]
    if selected_club != 'All':
        filtered = filtered[filtered['Club'] == selected_club]

    #show metric cards
    cols = st.columns((1, 1, 1,3), gap='medium')
    with cols[0]:
        avg = filtered[selected_avg_metric].mean()
        if not pd.isna(avg):
            custom_metric_card(label=f"Average {selected_avg_metric}", value=f"{avg:.1f}")

    with cols[1]:
        max = filtered[selected_max_metric].max()
        if not pd.isna(max):
            custom_metric_card(label=f"Max {selected_max_metric}", value=f"{max:.1f}")

    with cols[2]:
        min = filtered[selected_min_metric].min()
        if not pd.isna(max):
            custom_metric_card(label=f"Min {selected_min_metric}", value=f"{min:.1f}")

    with cols[3]:
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
 