import streamlit as st
from st_pages import Page, show_pages, add_page_title

import os,sys,inspect

st.set_page_config(layout="wide")

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATA_PATH = os.path.dirname(currentdir)

from PIL import Image
with st.container():
    cnbc_logo = Image.open('assets/cnbc_logo.png')
    st.image(cnbc_logo, width=50)

# show_pages(
#     [
#         Page(f"app/main.py", "Home Page", "🏠"),

#     ]
# )
show_pages(
    [
        Page(f"app/main.py", "Home Page", "🏠"),
        Page(f"app/all_social_media_overview.py", "All Media Overview", "🏠"),
        Page(f"app/pages/twitter/overview_twitter.py", " Twitter Performance Overview", "🔭"),
        Page(f"app/pages/twitter/twitter_feeds.py", "Twitter Feeds", "👁️"),
        Page(f"app/pages/twitter/text_analysis_twitter.py", "Twitter Content Analysis", "⚖️"),
        Page(f"app/pages/instagram/overview_instagram.py", " Instagram Performance Overview", "🔭"),
        Page(f"app/pages/instagram/instagram_feeds.py", " Instagram Feeds", "👁️"),
        Page(f"app/pages/instagram/text_analysis_instagram.py", " Instagram Content Analysis", "👁️")
    ]
)



# Main Description
st.markdown("## 👋 Welcome to Social Network Analysis Dashboard")
st.markdown("### Giving the best insights for your social media campaign strategy!")
st.markdown("Developed by Product Data Team")
st.markdown("The app is still under development. Please reach us if you have any comments or suggestions.")

# Description of the features.
st.markdown(
    """
    ### Select on the left panel what you want to explore:
    -  Performance Overview Metrics:
        - Popularity Score -> total likes + total retweets
        - Controversiality Score -> total quote tweets + total replies
        - Impression -> how many times our tweets are being viewed
    - Text Analysis:
        - Tweets clustering
        - Entity recognition
        - Sentiment Analysis
    """
)