import streamlit as st
import plotly.express as px
from datetime import date
import altair as alt
import pandas as pd
from utils_twitter import *
from utils_instagram import *




st.set_page_config(
    page_title="All Media Overview",
    page_icon="👋",
)

# Create a sidebar with a date input
start_date = st.sidebar.date_input("Start date", value=date(2023, 3, 4))
end_date = st.sidebar.date_input("End date", value=date(2023, 3, 7))

df_tweet, df_reply = load_data_twitter()

# Convert date column to datetime format
df_tweet['date'] = pd.to_datetime(df_tweet['date'])
df_reply['date_only'] = pd.to_datetime(df_reply['date_only'])


# Convert the date inputs to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the data based on the date input
result_dict = filtering_wrap(df_tweet,df_reply, start_date, end_date)

#score card

score_card_dict = score_card_wrap(result_dict["tweet_per_date"],result_dict["tweet_per_date_previous"],
                                  result_dict["popularity_per_date"],result_dict["popularity_per_date_previous"],
                    result_dict["controversiality_per_date"], result_dict["controversiality_per_date_previous"],
                    result_dict["impressions_per_date"], result_dict["impressions_per_date_previous"],
                    result_dict["clicks_per_date"], result_dict["clicks_per_date_previous"])

total_tweets = score_card_dict["total_tweets"]
tweet_diff = score_card_dict["total_tweets_diff"]
total_popularity = score_card_dict["total_popularity"]
popularity_diff = score_card_dict["total_popularity_diff"]
total_controversiality = score_card_dict["total_controversiality"]
controversiality_diff = score_card_dict["total_controversiality_diff"]
total_impressions = score_card_dict["total_impressions"]
impressions_diff = score_card_dict["total_impressions_diff"]
total_clicks = score_card_dict["total_clicks"]
clicks_diff = score_card_dict["total_clicks_diff"]

st.markdown("## CNBC Twitter Performance Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Tweets", f"{total_tweets}", '{:.1%}'.format(tweet_diff))
col2.metric("Popularity", f"{total_popularity}", '{:.1%}'.format(popularity_diff))
col3.metric("Controversiality", f"{total_controversiality}", '{:.1%}'.format(controversiality_diff))
col4.metric("Impression", f"{format_large_number(total_impressions)}", '{:.1%}'.format(impressions_diff))
col5.metric("Link Clicked", f"{total_clicks}", '{:.1%}'.format(clicks_diff))




df_post, df_summary = load_data_instagram()

# Convert date column to datetime format
df_post['date'] = pd.to_datetime(df_post['date'])
df_summary['date'] = pd.to_datetime(df_summary['date'])


# Convert the date inputs to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the data based on the date input
result_dict = filtering_wrap_ig(df_post,start_date, end_date)

#score card

score_card_dict = score_card_wrap_ig(result_dict["tweet_per_date"],result_dict["tweet_per_date_previous"],
                                  result_dict["interactions_per_date"],result_dict["interactions_per_date_previous"],
                    result_dict["replies_per_date"], result_dict["replies_per_date_previous"],
                    result_dict["impressions_per_date"], result_dict["impressions_per_date_previous"],
                    result_dict["reach_per_date"], result_dict["reach_per_date_previous"])

total_tweets = score_card_dict["total_tweets"]
tweet_diff = score_card_dict["total_tweets_diff"]
total_interactions = score_card_dict["total_interactions"]
interactions_diff = score_card_dict["total_interactions_diff"]
total_replies = score_card_dict["total_replies"]
replies_diff = score_card_dict["total_replies_diff"]
total_impressions = score_card_dict["total_impressions"]
impressions_diff = score_card_dict["total_impressions_diff"]
total_reach = score_card_dict["total_reach"]
reach_diff = score_card_dict["total_reach_diff"]

st.markdown("## CNBC Instagram Performance Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Posts", f"{total_tweets}", '{:.1%}'.format(tweet_diff))
col2.metric("Interactions", f"{format_large_number(total_interactions)}", '{:.1%}'.format(interactions_diff))
col3.metric("Comments", f"{total_replies}", '{:.1%}'.format(replies_diff))
col4.metric("Impressions", f"{format_large_number(total_impressions)}", '{:.1%}'.format(impressions_diff))
col5.metric("Reaches", f"{format_large_number(total_reach)}", '{:.1%}'.format(reach_diff))

