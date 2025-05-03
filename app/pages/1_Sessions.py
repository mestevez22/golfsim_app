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
from plotly.subplots import make_subplots
from datetime import timedelta
from style import custom_sidebar_css, custom_metric_card
from process import Preprocessor


class SessionsPage:
    def __init__(self):
        self.data = Preprocessor().get_data()
        self.tab_labels = ['Performance', 'Angle of Attack', 'Smash Factor', 'Spin Analysis'] #tab labels
        self.club_filter_opts = ['All'] + list(self.data['Club'].unique()) #club type filter options 
        self.start_date = self.data['Date'].min()
        self.end_date = self.data['Date'].max() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        self.not_metrics = ['Date', 'Unnamed: 0', 'Club', 'Decent']
        self.metric_opts = [i for i in set(self.data.columns) if i not in self.not_metrics]
        self.spin_metrics = ['BackSpin', 'SideSpin', 'rawSpinAxis']
        self.filtered_data = None
    
    #filter data based on inputs
    def filter_data(self, date_range, selected_club):
        filtered = self.data[self.data['Date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

        if isinstance(selected_club, list):
            if 'All' in selected_club and len(selected_club) == 1:
                pass  
            else:
                filtered = filtered[filtered['Club'].isin(selected_club)]
        else:
            if selected_club != 'All':
                filtered = filtered[filtered['Club'] == selected_club]

        return filtered


    
    #define multiselection filter for plotly charts 
    def club_multiselect(self, key: str):
        clubs = st.multiselect(
            "Filter clubs", 
            self.club_filter_opts, 
            default=self.club_filter_opts,
            key=key
        )
        if 'All' in clubs:
            return list(self.data['Club'].unique())
        return clubs

    def all_club_data(self):
        return self.filter_data(self.date_range, 'All') 

    #render tabs 
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
                if label == 'Performance':
                    self.render_perform_tab()
                elif label == 'Angle of Attack':
                    self.render_AoA_tab()
                elif label == 'Smash Factor':
                    self.render_smash_tab()
                else:
                    self.render_spin_tab()
    
    ############## RENDER TAB 1 - PERFORMANCE METRICS ############## 
    def render_perform_tab(self):
        st.markdown("## Performance Metrics")
        col_filters = st.columns(2)

        with col_filters[0]:
            self.selected_club = st.selectbox("Filter by Club", self.club_filter_opts, index=0, key='club_filter_tab1')

        with col_filters[1]:
            self.selected_metric = st.selectbox("Select Metric", self.metric_opts, key='selected_metric_inline')

        filtered_data = self.filter_data(self.date_range, self.selected_club)  #filter data based on selections

        #show metric cards
        cols = st.columns((1, 4), gap='small')
        with cols[0]:
            metric_data = filtered_data[self.selected_metric]
            min_val = metric_data.min()
            avg_val = metric_data.mean()
            max_val = metric_data.max()
            std_val = metric_data.std()
            count_val = metric_data.count()

            if not pd.isna(min_val):
                custom_metric_card(label="Minimum", value=f"{min_val:.1f}")
            if not pd.isna(avg_val):
                custom_metric_card(label="Average", value=f"{avg_val:.1f}")
            if not pd.isna(max_val):
                custom_metric_card(label="Maximum", value=f"{max_val:.1f}")
            if not pd.isna(std_val):
                custom_metric_card(label="Standard Deviation", value=f"{std_val:.1f}")
                st.caption(f"Total Shots: {count_val}")
        
        #render distancetopin trend chart
        with cols[1]:
            st.markdown("### Average Distance to Pin Over Time by Club")
            #chart multiselection filter for clubs 
            selected_clubs = self.club_multiselect("perform_chart_club_filter")

            filtered_chart = filtered_data[filtered_data['Club'].isin(selected_clubs)]
            grouped = (
                filtered_chart
                .groupby(['Date', 'Club'])['DistanceToPin']
                .mean()
                .reset_index()
            )

            fig = px.scatter(
                grouped,
                x='Date',
                y='DistanceToPin',
                color='Club',
                trendline='ols',
                labels={'DistanceToPin': 'Avg Distance to Pin (Yards)'},
                title=''
            )
            fig.update_yaxes(rangemode='tozero')
            st.plotly_chart(fig, use_container_width=True)


    ############## RENDER TAB 2 - ANGLE OF ATTACK ANALYSIS ############## 
    def render_AoA_tab(self):
        st.markdown("## Angle of Attack vs. Carry Distance vs. Peak Height")
        all_club_chart = self.all_club_data()
        #all_club_chart = self.filter_data(self.date_range, 'All')  
        aoa_range = [all_club_chart['AoA'].min() - 1, all_club_chart['AoA'].max() + 1]
    

        #-----chart 1: AoA vs Peak & Carry-------#
        #with cols[0]:
            #multiselection for clubs 
        selected_clubs = self.club_multiselect("AoA_chart_club_filter")

        #filter based on club selection
        filtered_chart = self.filter_data(self.date_range, selected_clubs)   #chart 1 only

        #create secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # plot dual axis scatter plot
        fig.add_trace(
            go.Scatter(x=filtered_chart['AoA'], y=filtered_chart['Carry'], name="Carry Distance", mode = 'markers', marker=dict(color='blue')),
            secondary_y=False)

        # Use add_trace function and specify secondary_y axes = True.
        fig.add_trace(
            go.Scatter(x=filtered_chart['AoA'], y=filtered_chart['PeakHeight'], name="Peak Height", mode= 'markers', marker=dict(color='red')),
            secondary_y=True)

        # Adding title text to the figure
        # fig4.update_layout(
        #     title_text="Multiple Y Axis in Plotly"
        # )

        # Naming x-axis
        fig.update_xaxes(title_text="Angle of Attack")

        # Naming y-axes
        fig.update_yaxes(title_text="<b>Carry Distance</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Peak Height</b> ", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

        #-----chart 2: AoA vs Club -------#
        cols = st.columns((4, 4), gap='medium')
        with cols[0]:
            grouped = (
                all_club_chart
                .groupby('Club', observed=True)
                .agg(AoA=('AoA', 'mean'), Count=('AoA', 'count'))
                .reset_index()
            )
            st.markdown("## Angle of Attacks vs. Club Type")
            #bubble chart 
            fig2 = px.scatter(
                grouped,
                x='Club',
                y='AoA',
                size='Count',#number of shots            
                color='Club',
                labels={'AoA': 'Mean Angle of Attack', 'Count': 'Shot Count'},
                title='',
                size_max=40            
            )

            fig2.update_yaxes(range= aoa_range)
            st.plotly_chart(fig2, use_container_width=True)
            
        #-----chart 3: AoA vs Club -------#
        with cols[1]:
            st.markdown("## Angle of Attacks vs. Carry Distance")
            
            #create bins 
            bin_edges = [0, 50, 75, 100, 125, 150, 175, 200,225]
            bin_labels = ['0–50', '50–75', '75–100', '100-125', '125-150', '150–175', '175–200', '200-225']
            all_club_chart = all_club_chart.copy()
            all_club_chart['CarryBin'] = pd.cut(all_club_chart['Carry'], bins=bin_edges, labels=bin_labels, right=False)
            binned = all_club_chart.groupby('CarryBin', observed=True).agg({'AoA': 'mean'}).reset_index()

            fig3 = px.bar(
            binned,
            x='CarryBin',
            y='AoA',
            color='CarryBin',
            labels={'CarryBin': 'Carry Distance (Yard Bins)', 'AoA': 'Average AoA'},
            title=''
        )
            fig3.update_yaxes(range = aoa_range)
            st.plotly_chart(fig3, use_container_width=True)

    ############## RENDER TAB 3 - SMASH FACTOR ANALYSIS ############## 

    def render_smash_tab(self):
        st.markdown(" ## Smash Factor Analysis")
        all_club_chart = self.all_club_data()
        selected_clubs = self.club_multiselect("smash_chart_club_filter")
        filtered_chart = all_club_chart[all_club_chart['Club'].isin(selected_clubs)]


        #create bins for smash factor
        bin_edges = [0.5, 1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6]
        bin_labels = ['0.5–1', '1–1.1', '1.1-1.15', '1.15-1.2','1.2-1.25', '1.25-1.3', '1.3–1.35', '1.35–1.4', '1.4-1.45', '1.45-1.5', '1.5-1.55', '1.55-1.6']
        filtered_chart = filtered_chart.copy()
        total_shots = filtered_chart.shape[0]
        filtered_chart['SmashBin'] = pd.cut(filtered_chart['SmashFactor'], bins=bin_edges, labels=bin_labels, right=False)
        binned = filtered_chart.groupby(['SmashBin'], observed=True).agg(AvgDistanceToPin=('DistanceToPin', 'mean'),
                                                                                 Count=('DistanceToPin', 'count')).reset_index()
        fig = px.bar(
            binned,
            x='SmashBin',
            y='AvgDistanceToPin',
            color='SmashBin',
            hover_data={
                'SmashBin': True,
                'AvgDistanceToPin': ':.3f',
                'Count': True
            },
            labels={
                'SmashBin': 'Smash Factor (ranges)',
                'DistanceToPin': 'Avg Distance to Pin',
                'Count' : 'Total Shots'
            },
            title=''
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Total Shots: {total_shots}")

    ############## RENDER TAB 4 - SPIN ANALYSIS ############## 
    def render_spin_tab(self):
        col_filters = st.columns(3)
        self.dist_metrics = ['Carry', 'TotalDistance']
        with col_filters[0]:
            self.selected_club = st.selectbox("Filter by Club", self.club_filter_opts, index=0, key='club_filter_tab4')

        with col_filters[1]:
            self.selected_dist = st.selectbox("Select a Distance Type", self.dist_metrics, key='selected_dist_inline')

        with col_filters[2]:
            self.selected_spin = st.selectbox("Select Metric", self.spin_metrics, key='selected_spin_inline')

        filtered_data = self.filter_data(self.date_range, self.selected_club)  #filter data based on selections

        grouped = (
            filtered_data
            .groupby(self.selected_spin, observed=True)
            .agg(Distance=(self.selected_dist, 'mean'), Count=(self.selected_dist, 'count'))
            .reset_index()
        )
        fig = px.scatter(
        filtered_data,
        x=self.selected_spin,
        y= self.selected_dist,
        trendline='lowess',  
        labels={self.selected_spin: self.selected_spin, self.selected_dist: f"{self.selected_dist} (Yards)"}
        )

        st.plotly_chart(fig, use_container_width=True)


#render page
SessionsPage().render()


    






 