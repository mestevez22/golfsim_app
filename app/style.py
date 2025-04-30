import streamlit as st

def custom_sidebar_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1E1E1E, #3A3A3A) !important;
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

    /* General widget containers*/
    .stContainer, .stSelectbox, .stDateInput, .stCheckbox, .stRadio, .stButton, .stTextInput {
        background: rgba(40, 40, 40, 0.85) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }

    /*  Make radio label stand out */
    label {
        font-weight: 600 !important;
        color: #CCCCCC !important;
    }

    /* smooth hover effect to buttons */
    button[kind="primary"] {
        background-color: #32CD32 !important;
        color: #000 !important;
        border: none !important;
        transition: background-color 0.3s ease-in-out;
    }

    button[kind="primary"]:hover {
        background-color: #28a428 !important;
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



