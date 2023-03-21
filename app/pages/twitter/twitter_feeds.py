import streamlit as st
import pandas as pd
from datetime import date
from utils_twitter import *

detik_tweet, detik_reply = load_data_twitter()

def set_data( start_date, end_date, sortby, filterby):
    data = detik_tweet.drop_duplicates(subset=['id'])
    data = data[ (data['date'] >= start_date) & (data['date'] <= end_date) ]

    if sortby == "Most Popular":
        data = data.sort_values(by='popularity_score', ascending=False)
    elif sortby == "Most Controversial":
        data = data.sort_values(by='controversiality_score', ascending=False)
    elif sortby == "Most Clicks":
        data = data.sort_values(by='clicks', ascending=False)


    if filterby == "All":
        data = data
    elif filterby == "Positive":
        data = data[data["sentiment_overall"] == 'positive']
    elif filterby == "Negative":
        data = data[data["sentiment_overall"] == 'negative']
    elif filterby == "Neutral":
        data = data[data["sentiment_overall"] == 'neutral']

    data = data.dropna()
    data = data.reset_index()
    return data

def set_feed(data):

    for index, row in data.iterrows():
        cont = st.container()
        c1, c2 = cont.columns(2)
        c1.markdown('%s ([link](%s))' % ("go to source:", row['link post']))
        c2.markdown(row['date'])
        
        cont.markdown('### %s' % row['content'])

        col1, col2, col3, col4 = cont.columns(4)

        if row['sentiment_overall'] == 'positive':
            col1.metric("Sentiment", "Positif ✅")
        elif row['sentiment_overall'] == 'negative':
            col1.metric("Sentiment", "Negatif ❌")
        elif row['sentiment_overall'] == 'neutral':
            col1.metric("Sentiment", "Neutral ⏸️")
        col2.metric("Popularity Score", "%s 👍🏻" % int(row['popularity_score']))
        col3.metric("Controversiality Score", "%s 💬" % int(row['controversiality_score']))
        col4.metric("Clicks", "%s 🚀" % int(row['clicks']))
        cont.markdown("""---""")



if __name__ == "__main__":
    st.markdown("# Twitter Content Feed")
    start_date = st.sidebar.date_input("Start date", value=date(2023, 3, 4)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 3, 6)).strftime("%Y-%m-%d")
    sortby = st.sidebar.selectbox(
        "Sort Content By",
        ("Most Popular", "Most Controversial", "Most Clicks")
    )

    filterby = st.sidebar.selectbox(
        "Filter Content By Sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    data = set_data(start_date, end_date, sortby, filterby)

    set_feed(data)