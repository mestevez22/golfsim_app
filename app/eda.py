# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import altair as alt
import plotly.express as px

#page setup
st.set_page_config(
    page_title="Golf Simulation Analysis - Garmin x GSPro",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

#inject css to background and sidebar 
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #2C2C2C, #0A0A0A) !important;
    color: #FFFFFF;  /* default */
}

/* match sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(to right, #1A1A1A, #0A0A0A) !important;
}

/* change sidebar title color */
[data-testid="stSidebar"] h1 {
    color: #32CD32 !important; /* neon green */
}

/* improve contrast */
.stSelectbox, .stDateInput, .stCheckbox {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

#load data 
path = Path(__file__).resolve().parent  # Path of script
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
    
    