import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import plotly.express as px
import streamlit as st
import requests
import streamlit.components.v1 as components
import random

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATA_PATH = os.path.dirname(currentdir)

@st.cache_data(ttl=300)
def load_data_instagram():
    detik_tweet = pd.read_csv(f"{DATA_PATH}/data/cnbc_ig_post_raw.csv")
    detik_reply = pd.read_csv(f"{DATA_PATH}/data/cnbc_ig_grouped_by_date.csv")
    return detik_tweet, detik_reply

@st.cache_data(ttl=300)
def load_data_instagram_clusters():
    detik_clusters = pd.read_csv(f"{DATA_PATH}/data/cnbc_ig_posts_txt_properties_ner.csv")
    detik_clusters = filter_values(detik_clusters,"entity",["cn","cnbc","com","cnbcindonesia","cnbcindonesiacom","bc"])
    return detik_clusters

def filter_values(df, column_name, values_to_filter):
    """
    Filters out rows from a column in a Pandas DataFrame that contain specific values.

    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    column_name (str): The name of the column to filter.
    values_to_filter (list): A list of values to filter out.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """
    # create a boolean mask to identify rows containing values to filter out
    mask = df[column_name].isin(values_to_filter)

    # filter out the rows containing the specified values
    df_filtered = df[~mask]
    
    return df_filtered

def filter_date_range(df, date_col, start_date, end_date):
    """Filter a pandas DataFrame based on a date range.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        date_col (str): The name of the date column in the DataFrame.
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.

    Returns:
        pandas.DataFrame: The filtered DataFrame.
    """
    # Convert date strings to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter DataFrame based on date range
    mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
    filtered_df = df.loc[mask]

    return filtered_df.sort_values(by=date_col, ascending=True)


def filter_by_date_with_previous_period(df,date_col, start_date, end_date):
    """Filter a DataFrame by a custom start date and end date, with a previous period included.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        start_date (str): The start date in yyyy-mm-dd format.
        end_date (str): The end date in yyyy-mm-dd format.

    Returns:
        pandas.DataFrame: A filtered DataFrame with previous period included, sorted by date ascending.
    """
    # Convert start and end dates to pandas datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Calculate start and end dates for previous period
    previous_start_date = start_date - timedelta(days=(end_date - start_date).days+1)
    previous_end_date = end_date - timedelta(days=(end_date - start_date).days+1)

    # Filter by date range
    filtered_df = df[(df[date_col] >= previous_start_date) & (df[date_col] <= previous_end_date)]

    # Sort by date ascending
    sorted_df = filtered_df.sort_values(date_col, ascending=True)

    return sorted_df


def count_by_group(df, group_col, count_col):
    """Group by a column and count the occurrences of each value.

    Args:
        df (pandas.DataFrame): The DataFrame to group by.
        group_col (str): The name of the column to group by.
        count_col (str): The name of the column to count.

    Returns:
        pandas.DataFrame: A DataFrame with the count of occurrences for each group.
    """
    counts = df.groupby(group_col)[count_col].count()
        # Convert the resulting Series to a DataFrame with a descriptive column name
    result = pd.DataFrame({'total_count': counts})

    # Reset the index to include the grouping column
    result.reset_index(inplace=True)

    return result


def sum_by_group(df, group_col, sum_col):
    """Group by a column and sum the values in another column.

    Args:
        df (pandas.DataFrame): The DataFrame to group by.
        group_col (str): The name of the column to group by.
        sum_col (str): The name of the column to sum.

    Returns:
        pandas.DataFrame: A DataFrame with the sum of values for each group.
    """
    
    # Group the DataFrame by the specified column and sum the other column
    grouped = df.groupby(group_col)[sum_col].sum()

    # Convert the resulting Series to a DataFrame with a descriptive column name
    result = pd.DataFrame({'total_value': grouped})

    # Reset the index to include the grouping column
    result.reset_index(inplace=True)

    # Return the result
    return result

@st.cache_data(ttl=300)
def filtering_wrap(df_tweet, start_date, end_date):
    # detik's tweet
    tweet_filtered = filter_date_range(df_tweet, "date", start_date, end_date)
    tweet_per_date = count_by_group(tweet_filtered, "date", "post id")
    #tweet_per_hour = count_by_group(tweet_filtered, "hour", "post id")
    tweet_filtered_previous = filter_by_date_with_previous_period(df_tweet, "date", start_date, end_date)
    tweet_per_date_previous = count_by_group(tweet_filtered_previous, "date", "post id")
    #tweet_per_hour_previous = count_by_group(tweet_filtered_previous, "hour", "post id")
    
    #interactions score
    interactions_per_date = sum_by_group(tweet_filtered, "date", "interactions")
    #interactions_per_hour = sum_by_group(tweet_filtered, "hour", "interactions")
    interactions_per_date_previous = sum_by_group(tweet_filtered_previous, "date", "interactions")
    #interactions_per_hour_previous = sum_by_group(tweet_filtered_previous, "hour", "interactions")
    
    #replies score
    replies_per_date = sum_by_group(tweet_filtered, "date", "comments")
    #replies_per_hour = sum_by_group(tweet_filtered, "hour", "replies")
    replies_per_date_previous = sum_by_group(tweet_filtered_previous, "date", "comments")
    #replies_per_hour_previous = sum_by_group(tweet_filtered_previous, "hour", "replies")
    
    #impressions score
    impressions_per_date = sum_by_group(tweet_filtered, "date", "impressions")
    #impressions_per_hour = sum_by_group(tweet_filtered, "hour", "impressions")
    impressions_per_date_previous = sum_by_group(tweet_filtered_previous, "date", "impressions")
    #impressions_per_hour_previous = sum_by_group(tweet_filtered_previous, "hour", "impressions")
    
        
    #reach score
    reach_per_date = sum_by_group(tweet_filtered, "date", "reach")
    #reach_per_hour = sum_by_group(tweet_filtered, "hour", "reach")
    reach_per_date_previous = sum_by_group(tweet_filtered_previous, "date", "reach")
    #reach_per_hour_previous = sum_by_group(tweet_filtered_previous, "hour", "reach")
    
    result_dict = {
        "tweet_per_date": tweet_per_date,
        #"tweet_per_hour": tweet_per_hour,
        "tweet_per_date_previous": tweet_per_date_previous,
        #"tweet_per_hour_previous": tweet_per_hour_previous,
        "interactions_per_date": interactions_per_date,
        #"interactions_per_hour": interactions_per_hour,
        "interactions_per_date_previous": interactions_per_date_previous,
        #"interactions_per_hour_previous": interactions_per_hour_previous,
        "replies_per_date": replies_per_date,
        #"replies_per_hour": replies_per_hour,
        "replies_per_date_previous": replies_per_date_previous,
        #"replies_per_hour_previous": replies_per_hour_previous,
        "impressions_per_date": impressions_per_date,
        #"impressions_per_hour": impressions_per_hour,
        "impressions_per_date_previous": impressions_per_date_previous,
        #"impressions_per_hour_previous": impressions_per_hour_previous,
        "reach_per_date": reach_per_date,
        #"reach_per_hour": reach_per_hour,
        "reach_per_date_previous": reach_per_date_previous,
        #"reach_per_hour_previous": reach_per_hour_previous,
                                                                }

    return result_dict
    





def add_date_column_and_concatenate(A, B,date_col="date"):
    """
    Adds a new period column to two Pandas DataFrames and concatenates them.

    Args:
        A (pandas.DataFrame): The first DataFrame to concatenate.
        B (pandas.DataFrame): The second DataFrame to concatenate.

    Returns:
        pandas.DataFrame: The concatenated DataFrame.

    """
    # Add new column to A and B
    A['period'] = 'This Period'
    B['period'] = 'Previous Period'
    B[date_col] = A[date_col]

    # Concatenate A and B
    concatenated_df = pd.concat([A, B], ignore_index=True)

    return concatenated_df 

def daily_tweet(df):
    df = df.rename(columns={"date_only": "date", "total_count": "total"})
    fig = px.line(df, x='date', y='total', title='Total Tweet Published per Day')
    return fig

def daily_interactions(df):
    df = df.rename(columns={"date_only": "date", "total_value": "total"})
    fig = px.line(df, x='date', y='total', title=' Tweet interactions per Day')
    return fig

def hourly_interactions(df):
    df = df.rename(columns={"total_value": "total"})
    fig = px.line(df, x='hour', y='total', title=' Tweet interactions per Hour').update_traces(line=dict(color='red'))
    return fig

def daily_engagement(df):
    df = df.rename(columns={"date_only": "date", "total_count": "total"})
    fig = px.line(df, x='date', y='total', title='Users Replies per Day')
    return fig


def hourly_engagement(df):
    df = df.rename(columns={"hour": "hour", "total_count": "total"})
    fig = px.line(df, x='hour', y='total', title='Users Replies per Hour').update_traces(line=dict(color="#f77f00"))
    return fig

def plot_metrics_by_date(df, color_1="blue", color_2="lightblue", y_title = "tweets published" ):
    # Rename the columns in the dataframe
    df = df.rename(columns={"date_only": "date", "total_count": y_title})

    # Create the line chart
    fig = px.line(df, x='date', y=y_title, color='period', symbol="period",
                  color_discrete_map={"This Period": color_1, "Previous Period": color_2}).update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white'
    )
    fig.show()
    


def altair_count_timeseries(concatenated_df, chart_title):
    data = concatenated_df
    data = data.rename(columns={"date_only": "date", "total_count": "total"})
    base = alt.Chart(data)
    line = base.mark_line().encode(
        x='date:T',
        y=alt.Y('total:Q', axis=alt.Axis(title='# of tweets published')),
        color= alt.Color('period:N', scale=alt.Scale(
            domain=['This Period', 'Previous Period', ],
            range=['#023e8a', '#00b4d8']
        )),
        tooltip=['date','total']
    ).properties(width=700)

    chart = line.properties(
        title=chart_title,
        height=400
    ).configure_legend(
        orient='top-left'
    ).configure_axis(
        grid=False
    )


    #chart_json = chart.to_json()
    return chart

def altair_sum_timeseries(concatenated_df, chart_title, color_1="red",color_2="#ffc8dd"):
    data = concatenated_df
    data = data.rename(columns={"date_only": "date", "total_value": "total"})
    base = alt.Chart(data)
    line = base.mark_line().encode(
        x='date:T',
        y=alt.Y('total:Q', axis=alt.Axis(title=chart_title)),
        color= alt.Color('period:N', scale=alt.Scale(
            domain=['This Period', 'Previous Period', ],
            range=[color_1, color_2]
        )),
        tooltip=['date','total']
    ).properties(width=700)

    chart = line.properties(
        title=chart_title,
        height=400
    ).configure_legend(
        orient='top-left'
    ).configure_axis(
        grid=False
    )


    #chart_json = chart.to_json()
    return chart
    
    
    
    

def fill_missing_rows(A, B):
    # Get a set of unique dates in A
    A_dates = set(A.iloc[:, 0].tolist())

    # Create a new dataframe B' with the same dates as A
    B_cols = B.columns.tolist()
    B_prime = pd.DataFrame(columns=B_cols)

    # Fill in the values from B where dates match
    if not B.empty:
        for i in range(B.shape[0]):
            date = B.iloc[i, 0]
            val = B.iloc[i, 1]
            B_prime = B_prime.append(pd.DataFrame([[date, val]], columns=B_cols), ignore_index=True)

    # Fill in any missing dates with 0
    for date in A_dates:
        if date not in B_prime.iloc[:, 0].tolist():
            B_prime = B_prime.append(pd.DataFrame([[date, 0]], columns=B_cols), ignore_index=True)

    # Sort the rows by date
    B_prime = B_prime.sort_values(by=B_cols[0])

    return B_prime


def check_same_rows(A, B):
    return A.shape[0] == B.shape[0]

def compute_now_previous(A,B,date_col="date"):
    if check_same_rows(A,B):
        concatenated_df = add_date_column_and_concatenate(A,B,date_col)
    else:
        B = fill_missing_rows(A,B)
        concatenated_df = add_date_column_and_concatenate(A,B,date_col)
    return concatenated_df


def calc_period_percent_diff(df):
    # Separate the dataframe into "This Period" and "Previous Period"
    this_period = df[df['period'] == 'This Period']
    prev_period = df[df['period'] == 'Previous Period']

    # Calculate the sum of values for each period
    this_period_sum = this_period.iloc[:, 1].sum()
    prev_period_sum = prev_period.iloc[:, 1].sum()

    # Calculate the percentage difference between the periods
    if prev_period_sum == 0:
        percent_diff = 0
    else:
        percent_diff = ((this_period_sum - prev_period_sum) / prev_period_sum)
    
    return this_period_sum, percent_diff


def score_card_wrap(tweet_per_date,tweet_per_date_previous,interactions_per_date,interactions_per_date_previous,
                    replies_per_date,replies_per_date_previous,
                    impressions_per_date,impressions_per_date_previous,
                    reach_per_date,reach_per_date_previous):
    total_tweets_concat = compute_now_previous(tweet_per_date,tweet_per_date_previous)
    total_tweets, total_tweets_diff = calc_period_percent_diff(total_tweets_concat)
    total_interactions_concat = compute_now_previous(interactions_per_date,interactions_per_date_previous)
    total_interactions, total_interactions_diff = calc_period_percent_diff(total_interactions_concat)
    total_replies_concat = compute_now_previous(replies_per_date,replies_per_date_previous)
    total_replies, total_replies_diff = calc_period_percent_diff(total_replies_concat)
    total_impressions_concat = compute_now_previous(impressions_per_date,impressions_per_date_previous)
    total_impressions, total_impressions_diff = calc_period_percent_diff(total_impressions_concat)
    total_reach_concat = compute_now_previous(reach_per_date,reach_per_date_previous)
    total_reach, total_reach_diff = calc_period_percent_diff(total_reach_concat)
    result_dict = {
        'total_tweets_concat':total_tweets_concat,
        'total_tweets': total_tweets,
        'total_tweets_diff': total_tweets_diff,
        'total_interactions': total_interactions,
        "total_interactions_concat": total_interactions_concat,
        'total_interactions_diff': total_interactions_diff,
        'total_replies': total_replies,
        'total_replies_concat': total_replies_concat,
        'total_replies_diff': total_replies_diff,
        'total_impressions': total_impressions,
        'total_impressions_concat': total_impressions_concat,
        'total_impressions_diff': total_impressions_diff,
        'total_reach': total_reach,
        'total_reach_concat': total_reach_concat,
        'total_reach_diff': total_reach_diff }
    return result_dict

def datetime_to_integer(date_object):
    """
    Convert a datetime object to an integer.
    :param date_object: the datetime object to convert (datetime)
    :return: the integer representation of the date (int)
    """
    return int(date_object.strftime('%Y%m%d'))


def generate_random_number(start, end, seed=None):
    """
    Generate a random integer between two given numbers (inclusive).
    :param start: the lower bound of the range (int)
    :param end: the upper bound of the range (int)
    :param seed: an optional seed value for the random number generator (int)
    :return: a random integer between start and end (inclusive)
    """
    if seed is not None:
        random.seed(seed)
    return random.randint(start, end)

def format_large_number(n):
    """
    Format large numbers as a string with a suffix indicating the magnitude (e.g. 1.23B for 1.23 billion).
    :param n: the number to format (int or float)
    :return: a string with the formatted number and magnitude suffix
    """
    suffixes = ['', 'K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    magnitude = 0
    while abs(n) >= 1000 and magnitude < len(suffixes) - 1:
        magnitude += 1
        n /= 1000.0
    result = '{:.2f}{}'.format(n, suffixes[magnitude])
    return result

def percentage_difference(a, b):
    """
    Calculate the percentage difference between two numbers.
    :param a: the first number (float or int)
    :param b: the second number (float or int)
    :return: the percentage difference between a and b (float)
    """
    diff = (a - b)
    avg = (a + b) / 2
    return (diff / avg)

class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=500)
    
    
class TweetReply(Tweet):
    def component(self):
        return components.html(self.text, height=800)
    
    
def plot_cluster(df_ner):
    # colors
    palette = px.colors.qualitative.Prism

    # create scatter plot with hover text
    fig = px.scatter(df_ner, x="x", y="y",color=df_ner["Cluster"].astype(str).values, color_discrete_sequence=palette,
                    hover_data=["text", "entity", "likes"],width=800, height=650)
    fig.update_layout(
        legend=dict(
            title=dict(text='Instagram Cluster')
        )
    )

    return fig


def cluster_reach(df_ner):
    df_plot_ner = df_ner.groupby(['Cluster']).agg({'reach': 'sum'}).rename(columns={'reach':'Total reach'}).reset_index().sort_values(by=['Total reach'], ascending = False).head(10)
    df_plot_ner = df_plot_ner.sort_values(by=['Total reach'])
    fig = px.bar(df_plot_ner,x="Cluster",y="Total reach", text_auto='.2s',width=750, height=350)
    return fig

def plot_entity_impressions(df_ner):
    df_plot_ner = df_ner.groupby(['entity']).agg({'impressions': 'sum'}).reset_index().rename(columns={'impressions':'Total Impressions'}).sort_values(by=['Total Impressions'], ascending = False).head(10)
    df_plot_ner = df_plot_ner.sort_values(by=['Total Impressions'])
    fig = px.bar(df_plot_ner, x="Total Impressions", y="entity", text_auto='.2s', width=350,)
    return fig

def plot_entity_interactions(df_ner):
    df_plot_ner = df_ner.groupby(['entity']).agg({'interactions': 'sum'}).reset_index().rename(columns={'interactions':'Total interactions'}).sort_values(by=['Total interactions'], ascending = False).head(10)
    df_plot_ner = df_plot_ner.sort_values(by=['Total interactions'])
    fig = px.bar(df_plot_ner, x="Total interactions", y="entity", text_auto='.2s', width=350,)
    return fig

def plot_entity_shares(df_ner):
    df_plot_ner = df_ner.groupby(['entity']).agg({'comments': 'sum'}).reset_index().rename(columns={'comments':'Total comments'}).sort_values(by=['Total comments'], ascending = False).head(10)
    df_plot_ner = df_plot_ner.sort_values(by=['Total comments'])
    fig = px.bar(df_plot_ner, x="Total comments", y="entity", text_auto='.2s', width=350)
    return fig

def most_published_entities(df_ner):
    df_plot_ner = df_ner.groupby(['entity']).agg({'entity': 'count'}).rename(columns={'entity':'Total Entities'}).reset_index().sort_values(by=['Total Entities'], ascending = False).head(10)
    df_plot_ner = df_plot_ner.sort_values(by=['Total Entities'])
    fig = px.bar(df_plot_ner, x="Total Entities", y="entity", text_auto='.2s', width=350)
    return fig


def get_top_entities(df, group_col, entity_col):
    # group by the specified columns and count the occurrences
    grouped = df.groupby([group_col, entity_col]).size().reset_index(name='count')

    # sort by group and count in descending order
    sorted_grouped = grouped.sort_values([group_col, 'count'], ascending=[True, False])

    # extract the top entity and count for each group
    result = sorted_grouped.groupby(group_col).head(1).reset_index(drop=True)
    result.columns = [group_col, 'Top Entity', 'Total Entity Count']

    return result

def plot_popular_entities_clusters(cluster_entity_df, group_col = "Cluster", entity_col= "entity" ):
    # create example dataframe
    df_plot = get_top_entities(cluster_entity_df,group_col,entity_col)
    fig = px.bar(df_plot, x='Cluster',y='Total Entity Count', color="Top Entity",width=850, height=350)
    fig.update_layout(
        legend=dict(
            title=dict(text='Top Entity')
        )
    )

    # display the chart
    return fig