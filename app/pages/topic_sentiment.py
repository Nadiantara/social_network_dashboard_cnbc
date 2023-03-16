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

st.plotly_chart(cluster_plot)
st.plotly_chart(cluster_clicks_plot)
st.plotly_chart(cluster_top_entities_plot)
