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
    page_title="Golf Simulation Analysis - Garmin x GSPro",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

#inject css to background and sidebar 
custom_sidebar_css()

#load data 
path = Path(__file__).resolve().parent.parent  #path of app's script
data = pd.read_csv(path / 'master.csv')
data['Month'] = pd.to_datetime(data['Date']).dt.month_name()
data['Date'] = pd.to_datetime(data['Date'])

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
    metrics = ['Carry', 'Total Distance', 'Ball Speed', 'Club Speed', 
                          'Smash Factor', 'Back Spin', 'Peak Height', 'Off line']
    selected_metric = st.selectbox('Primary Metric', metrics,
                                  index=3)  #default to club speed
    
    