import streamlit as st
import pandas as pd
from datetime import date
from utils_instagram import *

detik_tweet = load_data_instagram_clusters()

def set_data( start_date, end_date, sortby, filterby):
    df = detik_tweet.drop_duplicates(subset=['post id'])
    data = df.dropna(subset=['text'])
    data = data[ (data['date'] >= start_date) & (data['date'] <= end_date) ]

    if sortby == "Most Popular":
        data = data.sort_values(by='interactions', ascending=False)
    elif sortby == "Most Comments":
        data = data.sort_values(by='comments', ascending=False)
    elif sortby == "Most Viewed":
        data = data.sort_values(by='impressions', ascending=False)


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
        
        lines = row['text'].splitlines()
        cont.markdown('### %s' % lines[0])
        c1, c2 = cont.columns(2)
        c1.markdown('%s ([link](%s))' % ("go to source:", row['link post']))
        c2.markdown(row['date'])
        cont.markdown('> %s' % " ".join(lines[1:]))
        # cont.markdown('> %s' % row['summary'])
        col1, col2, col3, col4 = cont.columns(4)

        if row['sentiment_overall'] == 'positive':
            col1.metric("Sentiment", "Positif ✅")
        elif row['sentiment_overall'] == 'negative':
            col1.metric("Sentiment", "Negatif ❌")
        elif row['sentiment_overall'] == 'neutral':
            col1.metric("Sentiment", "Neutral ⏸️")
        col2.metric("Popularity Score", "%s 👍🏻" % int(row['interactions']))
        col3.metric("Commented", "%s 💬" % int(row['comments']))
        col4.metric("Impressions", "%s 🚀" % format_large_number(int(row['impressions'])))
        cont.markdown("""---""")



if __name__ == "__main__":
    st.markdown("# Instagram Content Feed")
    start_date = st.sidebar.date_input("Start date", value=date(2023, 3, 4)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 3, 6)).strftime("%Y-%m-%d")
    sortby = st.sidebar.selectbox(
        "Sort Content By",
        ("Most Popular", "Most Comments", "Most Viewed")
    )

    filterby = st.sidebar.selectbox(
        "Filter Content By Sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    data = set_data(start_date, end_date, sortby, filterby)

    set_feed(data)