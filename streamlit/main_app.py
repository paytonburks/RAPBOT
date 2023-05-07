import streamlit as st
import pandas as pd
import matplotlib as plt
import numpy as np
import utils
from sklearn import preprocessing

df = pd.read_csv('dfs/FINAL.csv')

# grouped by tweet sentiment analysis
grouped_sent = df.groupby("tweet_sent")

# reply sent data
ai_neg = df['reply_sent'].value_counts()['negative']
ai_neut = df['reply_sent'].value_counts()['neutral']
ai_pos = df['reply_sent'].value_counts()['positive']
# negative vs neutral vs positive bar chart
x = []
y = []
y2 = []
for group, d in grouped_sent:
    if group == 'negative':
        y2.append(ai_neg)
    elif group == 'neutral':
        y2.append(ai_neut)
    elif group == 'positive':
        y2.append(ai_pos)

    x.append(group)
    y.append(len(d))

data = {"Sentiment": x, "Origin Count": y, "Reply Count": y2}
sent_df = pd.DataFrame(data=data)
# df without missing data
df_no_na = df.dropna()
grouped_2 = df.groupby('tweet_sent')

# random forest object
rf = utils.random_forest_gen(df)

t1, t2, t3, t4 = st.tabs(["Home", "Exploratory Data Analysis", "ML Predictors", "SlattBot"])

with t1:
    st.write("""
    # Twitter AI Sentiment Analysis
    ### Created by Payton Burks
    (Developed on [@youngthug](https://twitter.com/youngthug) tweets)
    """)
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("streamlit/thugbot.png", caption="image generated by StarryAI", width=300)
    st.write("""
    This web app displays twitter data insights from a community representative of \
        fanatics. I aim to explore the reply differences between diehard fans and AI\
        representative of an average user.
    """)

with t2:
    st.write("""
    # Exploratory Data Analysis
    """)

    st.write("""A simple scatterplot displaying growth
    """)
    st.image('./EDA/tweets_over_time.png')

    st.write("""Sentiment Analysis for Tweets
    """)
    st.bar_chart(data=sent_df.set_index("Sentiment"), y=None)

    st.write("""Number of replies based on how strong the tweet sentiment is (2017 onward)
    """)
    sent_strength_sel = st.selectbox(label='Sentiment', options=['All', 'Negative', 'Neutral', 'Positive'])
    if sent_strength_sel == "All":
        st.image('./EDA/all_sentiment.png')
    elif sent_strength_sel == "Negative":
        st.image('./EDA/negative replies.png')
    elif sent_strength_sel == "Neutral":
        st.image('./EDA/neutral replies.png')
    elif sent_strength_sel == "Positive":
        st.image('./EDA/positive replies.png')

with t3:
    st.write(""" 
    # Machine Learning 
    """)
    st.write("""Reply Sentiment Predictor
    """)
    st.write("""Enter some tweet stats
    """)
    likes = st.text_input("Likes", key=1)
    if likes:
        likes = int(likes)
    rep = st.text_input("Replies", key=2)
    if rep:
        rep = int(rep)
    rts = st.text_input("Retweets", key=3)
    if rts:
        rts = int(rts)
    source = st.selectbox(label="Source", options=df['source'].unique(), key=4)
    time_of_day = st.selectbox(label="Time of Day", options=df['time_of_day'].unique(), key=5)
    month = st.selectbox(label="Month", options=df['month'].unique(), key=6)
    tweet_sent = st.selectbox(label="Sentiment", options=df['tweet_sent'].unique(), key=7)
    tweet_score = st.slider(label="Choose how strong your sentiment is:", min_value=0.5, max_value=float(1), value=0.75, key=8)

    if st.button(label="Go"):
        if likes and rep and rts and source and time_of_day and month and tweet_sent and tweet_score:
            row = []
            row.extend(['', likes, rep, rts, source, '', '',  time_of_day, month, tweet_sent, tweet_score, '', ''])
            df.loc[len(df)] = row
            pred, acc = utils.random_forest_gen(df, pred=row)
            st.text("Prediction: "+str(pred))
            st.text("Accuracy: "+str(round(acc, 4)))
        else: 
            st.write("Error in tweet stat values; try again")    

with t4:
    st.write(""" 
    # SlattBot tweet generator
    """)
    prompt = st.text_input("Input a prompt")
    tweet = utils.slatt_bot_gen(str(prompt))
    st.text(tweet)