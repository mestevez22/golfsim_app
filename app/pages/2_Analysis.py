#load packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from style import custom_sidebar_css, custom_metric_card
from process import Preprocessor
from rf_model import RunRandomForest
from utils import filter_data


class AnalysisPage():
    def __init__(self):
        self.data = Preprocessor.get_data()
        self.start_date = self.data['Date'].min()
        self.end_date = self.data['Date'].max() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        self.distances_opts = ['Carry', 'TotalDistance']
        self.irons = [i for i in self.data['Club'].unique() if i.startswith("I")]
        self.clubgroup_opts = ['All', 'Irons', 'Driver']
        self.exclude_opts = [i for i in self.data.columns if i != 'Date']
        self.tab_labels = ['Insights & Trends', 'Random Forest Analysis', 'Time Series Forecast', 'Optimization']
        self.exclude_cols = None

    
    def load_rf_results(self, selected_target, selected_exclude_cols, selected_club_type):
        if selected_club_type == 'Irons':
            clubs = self.irons
            self.data = filter_data(self.date_range, clubs)
        elif selected_club_type == 'Driver':
            clubs = 'DR'
            self.data = filter_data(self.date_range, clubs)
        else:
            self.data = filter_data(self.date_range, 'All') 


        reg = RunRandomForest(self.data, selected_target, exclude_cols= selected_exclude_cols)
        reg.onehotencode()
        reg.split_data(size = 0.3)
        reg.fit(cv=5)
        self.oob, self.mse, self.r2 = reg.evaluate()
        self.feat_imp = reg.feature_importance(top_n=10)
        self.shap_vals = reg.shap_values()
        return self.oob, self.mse, self.r2, self.feat_imp, self.shap_vals
    
    
    def clubgroup_multiselect(self, key: str):
        clubgroup = st.multiselect(
            "Filter club type", 
            self.clubgroup_opts, 
            default=self.clubgroup_opts,
            key=key
        )
        return clubgroup
    
    def render(self):
        st.set_page_config(
            page_title="Sessions Overview",
            page_icon="⛳",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        #inject custom css 
        custom_sidebar_css()

        #set up sidebar 
        with st.sidebar:
            st.title('Golf Simulation Statistics')
            
            #filter for date change
            self.date_range = st.date_input('Date Range', [self.start_date, self.end_date])
            if len(self.date_range) != 2:
                st.stop() 

        #create tabs and tab methods 
        tabs = st.tabs(self.tab_labels)
        for tab, label in zip(tabs, self.tab_labels):
            with tab:
                if label == 'Insights & Trends':
                    self.render_insights_tab()
                elif label == 'Random Forest Analysis':
                    self.render_rf_tab()
                elif label == 'Time Series Forecast':
                    self.render_ts_tab()
                else:
                    self.render_optim_tab()

    ############## RENDER TAB 1 - OVERVIEW OF INSIGHTS ############## 
    def render_insights_tab(self):
        pass

    ############## RENDER TAB 2 - RANDOM FOREST ############## 
    def render_rf_tab(self):
        st.markdown("## Random Forest Analysis")
        col_filters = st.columns(4)

        with col_filters[0]:
            self.selected_target = st.selectbox("Select a Target", self.distances_opts, index=0, key='target_filter_tab')

        with col_filters[1]:
            self.selected_club_type = st.selectbox("Select Club Type", self.clubgroup_opts, key='selected_clubtype_inline')
        
        with col_filters[2]:
            current_exclude_opts = [col for col in self.data.columns if col not in ['Date', self.selected_target]]
            self.selected_exclude_cols = st.multiselect(
                "Exclude Features", 
                current_exclude_opts, 
                default=current_exclude_opts,
                key='rf_exclude_filter'
            )

        filtered_data = filter_data(self.date_range, self.selected_club_type)  #filter data based on selections


        
        

        



