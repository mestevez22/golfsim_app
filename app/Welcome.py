# Load packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from pathlib import Path
from style import custom_sidebar_css


#page setup
st.set_page_config(
    page_title="SimShot Analytics",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_sidebar_css() #apply custom css for sidebar

st.write("# Welcome to SimShot Analytics 👋")
with st.sidebar:
    st.success("Choose a view below")
    #st.page_link('app.py', label='Welcome', icon='🔥')
    #st.page_link('pages/sessions.py', label='Sessions Overview', icon='🛡️')
    

