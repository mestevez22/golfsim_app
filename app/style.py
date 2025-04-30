import streamlit as st

def custom_sidebar_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0A0A0A, #2C2C2C) !important;
        color: #FFFFFF;  /* default */
    }

    /* match sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(to right, #0A0A0A, #1A1A1A) !important; /* #1A1A1A */
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

def custom_metric_card(label, value):
    st.markdown(f"""
        <div style="background-color:#a60000; width:200px; height:150px;
                    display:flex; flex-direction:column; justify-content:center;
                    align-items:center; border-radius:5px; border:5px solid #000;">
            <div style="font-weight:bold; text-align:center;">{label}</div>
            <div style="font-size:24px; font-weight:bold;">{value}</div>
        </div>
    """, unsafe_allow_html=True)



