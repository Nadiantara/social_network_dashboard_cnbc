# Contents of ~/my_app/pages/page_2.py
import streamlit as st
import plotly.express as px
from datetime import date
import pandas as pd
from utils_twitter import *




st.set_page_config(page_title="Popular Tweets and Replies", page_icon="📈")

st.markdown("# Popular Tweets and Replies")
# Create a sidebar with a date input
start_date = st.sidebar.date_input("Start date", value=date(2023, 3, 4))
end_date = st.sidebar.date_input("End date", value=date(2023, 3, 6))

df_tweet, df_reply = load_data_twitter()

# Convert date column to datetime format
df_tweet['date'] = pd.to_datetime(df_tweet['date'])
df_reply['date_only'] = pd.to_datetime(df_reply['date_only'])


# Convert the date inputs to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the data based on the date input
result_dict = filtering_wrap(df_tweet, df_reply, start_date, end_date)


top_popular_tweets_list = result_dict["top_popular_tweets"]["id"].to_list()
top_popular_replies_list = result_dict["top_popular_replies"]["reply_id"].to_list()
top_popular_replies_name = result_dict["top_popular_replies"]["user_name"].to_list()
#concatenated_df = add_date_column_and_concatenate(tweet_per_date, tweet_per_date_previous)

# Create a two-column layout with the charts
with st.container():
   with st.expander("See Popular Tweets"):
      col1, col2 = st.columns(2)
      with col1:
         st.markdown("### 1st Tweet")
         t = Tweet(f"https://twitter.com/cnbcindonesia/status/{top_popular_tweets_list[0]}").component()

      with col2:
         st.markdown("### 2nd Tweet")
         t = Tweet(f"https://twitter.com/cnbcindonesia/status/{top_popular_tweets_list[1]}").component()
         
      col3, col4 = st.columns(2)

      with col3:
         st.markdown("### 3rd Tweet")
         t = Tweet(f"https://twitter.com/cnbcindonesia/status/{top_popular_tweets_list[2]}").component()

      with col4:
         st.markdown("### 4th Tweet")
         t = Tweet(f"https://twitter.com/cnbcindonesia/status/{top_popular_tweets_list[3]}").component()
 
with st.container():  
   with st.expander("See Popular Replies"):
      col5, col6 = st.columns(2)
      with col5:
         st.markdown("### 1st Reply")
         t = TweetReply(f"https://twitter.com/{top_popular_replies_name[0]}/status/{top_popular_replies_list[0]}").component()

      with col6:
         st.markdown("### 2nd Reply")
         t = TweetReply(f"https://twitter.com/{top_popular_replies_name[1]}/status/{top_popular_replies_list[1]}").component()
         
      col7, col8 = st.columns(2)
      with col7:
         st.markdown("### 3rd Reply")
         t = TweetReply(f"https://twitter.com/{top_popular_replies_name[0]}/status/{top_popular_replies_list[2]}").component()

      with col8:
         st.markdown("### 4th Reply")
         t = TweetReply(f"https://twitter.com/{top_popular_replies_name[1]}/status/{top_popular_replies_list[3]}").component()