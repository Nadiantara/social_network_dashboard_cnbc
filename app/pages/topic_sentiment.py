import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd
from utils import *



st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")

df_cluster = load_data_clusters()

cluster_plot = plot_cluster(df_cluster)
cluster_top_entities_plot = plot_popolar_entities_clusters(df_cluster)
cluster_clicks_plot = cluster_clicks(df_cluster)
top_entities_impressions = plot_entity_impressions(df_cluster)
top_entities_clicks = plot_entity_clicks(df_cluster)
top_published_entities = most_published_entities(df_cluster)
top_entities_likes = plot_entity_likes(df_cluster)

st.plotly_chart(cluster_plot)
st.plotly_chart(cluster_clicks_plot)
st.plotly_chart(cluster_top_entities_plot)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### Top 10 Entities by Impression")
    st.plotly_chart(top_entities_impressions)

with col2:
    st.markdown("##### Top 10 Entities by Clicks")
    st.plotly_chart(top_entities_clicks)
    
col3, col4 = st.columns(2)
with col3:
    st.markdown("##### Top 10 Most Published Entities")
    st.plotly_chart(top_published_entities)

with col4:
    st.markdown("##### Top 10 Entities by Likes")
    st.plotly_chart(top_entities_likes)