# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
import plotly.express as px
from style import custom_sidebar_css

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
    df['DistanceToPin_Yrds'] = df['DistanceToPin_Yrds'].apply(lambda x: x.split(' ')[0])
    return df

data = get_master_data()

#set sidebar up
with st.sidebar:
    st.title('Golf Simulation Statistics')
    
    #filter for date change
    min_date = data['Date'].min().date()
    max_date = data['Date'].max().date()
    date_range = st.date_input('Date Range', [min_date, max_date])
    
    #club type filter 
    club_list = ['All'] + sorted(list(set(data['Club'])))
    selected_club = st.selectbox('Select Club', club_list, index=0)
    
    #select metrics 
    not_metrics = ['Date', 'Month', 'Unnamed: 0', 'Club', 'DistanceToPin_Yrds', 'Decent']
    #metrics = ['Carry', 'Path']
    metric_opts = ['All'] + [i for i in set(data.columns) if i not in not_metrics]
    selected_metric = st.selectbox('Primary Metric', metric_opts,
                                  index=0)  #default to All
    
    
#filter data 
filtered = data[data['Date'].between(pd.to_datetime(date_range[0]), 
                                        pd.to_datetime(date_range[1]))]

#filter for club if not all
if selected_club != 'All':
    filtered = filtered[filtered['Club'] == selected_club]

if selected_metric == 'All':
    # Show multiple metrics
    numeric_metrics = [col for col in filtered.columns if col not in not_metrics]
    cols = st.columns((1,1,2,2), gap = 'medium')  # You can adjust how many columns to show metrics across
    for i, metric in enumerate(numeric_metrics):
        with cols[i % 2]:
            avg = filtered[metric].mean()
            st.metric(label=f"Avg {metric}", value=f"{avg:.1f}")
else:
    # Show single selected metric
    col = st.columns((2, 4, 2), gap='medium')
    with col[0]:
        avg = filtered[selected_metric].mean()
        st.metric(f"Average {selected_metric}", f"{avg:.1f}")
