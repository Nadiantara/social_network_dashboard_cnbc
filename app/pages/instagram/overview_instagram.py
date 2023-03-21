import streamlit as st
import plotly.express as px
from datetime import date
import altair as alt
import pandas as pd
from utils_instagram import *




st.set_page_config(
    page_title="Instagram Dashboard Overview",
    page_icon="👋",
)

# Create a sidebar with a date input
start_date = st.sidebar.date_input("Start date", value=date(2023, 3, 4))
end_date = st.sidebar.date_input("End date", value=date(2023, 3, 7))

df_tweet, df_summary = load_data_instagram()

# Convert date column to datetime format
df_tweet['date'] = pd.to_datetime(df_tweet['date'])
df_summary['date'] = pd.to_datetime(df_summary['date'])


# Convert the date inputs to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter the data based on the date input
result_dict = filtering_wrap_ig(df_tweet,start_date, end_date)

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

#random seed impression
random_seed_start = datetime_to_integer(start_date) 
random_seed_end =  datetime_to_integer(end_date)
number_start = generate_random_number(1400000,1600000,random_seed_start)
number_end = generate_random_number(1400000,1600000,random_seed_end)
impression_diff = percentage_difference(number_start,number_end)

#random seed link reach
random_seed_start_link_clicked = datetime_to_integer(start_date) 
random_seed_end_link_clicked  =  datetime_to_integer(end_date)
number_start_link_clicked  = generate_random_number(3500,5000,random_seed_start_link_clicked)
number_end_link_clicked  = generate_random_number(3500,6000,random_seed_end_link_clicked)
link_clicked_diff = percentage_difference(number_start_link_clicked,number_end_link_clicked)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Posts", f"{total_tweets}", '{:.1%}'.format(tweet_diff))
col2.metric("Comments", f"{total_replies}", '{:.1%}'.format(replies_diff))
col3.metric("Interactions", f"{format_large_number(total_interactions)}", '{:.1%}'.format(interactions_diff))
col4.metric("Impressions", f"{format_large_number(total_impressions)}", '{:.1%}'.format(impressions_diff))
col5.metric("Reaches", f"{format_large_number(total_reach)}", '{:.1%}'.format(reach_diff))


tweet_concat = score_card_dict["total_tweets_concat"]
interactions_concat = score_card_dict["total_interactions_concat"]
replies_concat = score_card_dict["total_replies_concat"]
impressions_concat = score_card_dict["total_impressions_concat"]
reach_concat = score_card_dict["total_reach_concat"]

published_tweets_plot = altair_count_timeseries(tweet_concat,"Total Daily Published Tweets")

tweets_impressions_plot = altair_sum_timeseries(impressions_concat,"Total Daily Tweets Impressions")

tweets_reach_plot = altair_sum_timeseries(reach_concat,"Total Daily Link reach")

popularities_plot = altair_sum_timeseries(interactions_concat, "Daily interactions Score")
#lineplot3 = hourly_interactions(result_dict["interactions_per_hour"])

controversialities_plot = altair_sum_timeseries(replies_concat,"Daily replies Score","#f77f00","#fcbf49")
#lineplot4 = daily_engagement(result_dict["reply_per_date"])
#lineplot5 = hourly_engagement(result_dict["reply_per_hour"])

st.altair_chart(published_tweets_plot, use_container_width=True)
st.altair_chart(tweets_impressions_plot, use_container_width=True)
st.altair_chart(tweets_reach_plot, use_container_width=True)

df_tweets_this_period = tweet_concat[tweet_concat["period"]=="This Period"]
df_tweets_interactions_this_period = interactions_concat[interactions_concat["period"]=="This Period"]
with st.container():
   with st.expander("See Published Tweets Table"):
        st.dataframe(df_tweets_this_period.iloc[:,:2])
        
st.altair_chart(popularities_plot, use_container_width=True)

with st.container():
   with st.expander("See Daily interactions Table"):
        st.dataframe(df_tweets_interactions_this_period.iloc[:,:2])
#st.plotly_chart(lineplot2)
#st.plotly_chart(lineplot3)
st.altair_chart(controversialities_plot, use_container_width=True)
#st.plotly_chart(lineplot5)
