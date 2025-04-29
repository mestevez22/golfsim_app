import streamlit as st
import pandas as pd
from pathlib import Path

def custom_sidebar_css():
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

