import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd
from utils_instagram import *



st.set_page_config(page_title="Twitter Content Analysis", page_icon="🌍")

st.markdown("## Instagram Content Analysis")

df_cluster = load_data_instagram_clusters()

cluster_plot = plot_cluster(df_cluster)
cluster_top_entities_plot = plot_popular_entities_clusters(df_cluster)
cluster_clicks_plot = cluster_reach(df_cluster)
top_entities_impressions = plot_entity_impressions(df_cluster)
top_entities_interactions = plot_entity_interactions(df_cluster)
top_published_entities = most_published_entities(df_cluster)
top_entities_shares = plot_entity_shares(df_cluster)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### Top 10 Entities by Impression")
    st.plotly_chart(top_entities_impressions)

with col2:
    st.markdown("##### Top 10 Entities by Interactions")
    st.plotly_chart(top_entities_interactions)
    
col3, col4 = st.columns(2)
with col3:
    st.markdown("##### Top 10 Most Published Entities")
    st.plotly_chart(top_published_entities)

with col4:
    st.markdown("##### Top 10 Entities by Comments")
    st.plotly_chart(top_entities_shares)
    
st.markdown("##### Instagram Text Clusters")     
st.plotly_chart(cluster_plot)
    
st.markdown("##### Instagram Clicks per Clusters")   
st.plotly_chart(cluster_clicks_plot)
st.markdown("##### Instagram Top Entities per Clusters")   
st.plotly_chart(cluster_top_entities_plot)
