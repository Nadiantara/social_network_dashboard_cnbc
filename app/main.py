import streamlit as st
import plotly.express as px
from datetime import date
import altair as alt
import pandas as pd
from utils import *




st.set_page_config(
    page_title="Twitter Dashboard Overview",
    page_icon="👋",
)

# Create a sidebar with a date input
start_date = st.sidebar.date_input("Start date", value=date(2022, 1, 8))
end_date = st.sidebar.date_input("End date", value=date(2022, 1, 14))

df_tweet, df_reply = load_data()

# Convert date column to datetime format
df_tweet['date_only'] = pd.to_datetime(df_tweet['date_only'])
df_reply['date_only'] = pd.to_datetime(df_reply['date_only'])


# Convert the date inputs to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the data based on the date input
result_dict = filtering_wrap(df_tweet, df_reply, start_date, end_date)

#score card

score_card_dict = score_card_wrap(result_dict["tweet_per_date"],result_dict["tweet_per_date_previous"],
                                  result_dict["popularity_per_date"],result_dict["popularity_per_date_previous"],
                    result_dict["controversiality_per_date"], result_dict["controversiality_per_date_previous"])

total_tweets = score_card_dict["total_tweets"]
tweet_diff = score_card_dict["total_tweets_diff"]
total_popularity = score_card_dict["total_popularity"]
popularity_diff = score_card_dict["total_popularity_diff"]
total_controversiality = score_card_dict["total_controversiality"]
controversiality_diff = score_card_dict["total_controversiality_diff"]

#random seed
random_seed_start = datetime_to_integer(start_date) 
random_seed_end =  datetime_to_integer(end_date)
number_start = generate_random_number(1400000000,1600000000,random_seed_start)
number_end = generate_random_number(1400000000,1600000000,random_seed_end)
impression_diff = percentage_difference(number_start,number_end)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweets", f"{total_tweets}", '{:.1%}'.format(tweet_diff))
col2.metric("Popularity Score", f"{total_popularity}", '{:.1%}'.format(popularity_diff))
col3.metric("Controversiality Score", f"{total_controversiality}", '{:.1%}'.format(controversiality_diff))
col4.metric("Impression", f"{format_large_number(number_start)}", '{:.1%}'.format(impression_diff))


tweet_concat = score_card_dict["total_tweets_concat"]
popularity_concat = score_card_dict["total_popularity_concat"]
controversiality_concat = score_card_dict["total_controversiality_concat"]

lineplot1 = altair_count_timeseries(tweet_concat,"Total Daily Published Tweets")
lineplot2 = altair_sum_timeseries(popularity_concat, "Daily Popularity Score")
lineplot3 = hourly_popularity(result_dict["popularity_per_hour"])

lineplot4 = altair_sum_timeseries(controversiality_concat,"Daily Controversiality Score","#f77f00","#fcbf49")
#lineplot4 = daily_engagement(result_dict["reply_per_date"])
lineplot5 = hourly_engagement(result_dict["reply_per_hour"])

st.altair_chart(lineplot1, use_container_width=True)
st.altair_chart(lineplot2, use_container_width=True)
#st.plotly_chart(lineplot2)
st.plotly_chart(lineplot3)
st.altair_chart(lineplot4, use_container_width=True)
st.plotly_chart(lineplot5)



