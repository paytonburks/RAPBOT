import pandas as pd
import re
from datetime import datetime


def get_time_label(time_str):
    time_dict = {
        "early morning": "05:00:00-07:59:59",
        "morning": "08:00:00-11:59:59",
        "afternoon": "12:00:00-16:59:59",
        "evening": "17:00:00-20:59:59",
        "night": "21:00:00-04:59:59"
    }

    time = datetime.strptime(time_str, "%H:%M:%S").time()
    for label, time_range in time_dict.items():
        start_time_str, end_time_str = time_range.split("-")
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        if (start_time <= time <= end_time) or (start_time > end_time and (start_time <= time or time <= end_time)):
            return label
    return "Unknown"

def thug_update_one():
    df = pd.read_csv("dfs/THUG_SENT_DF.csv")
    tweets = df['tweet'].\
              str.replace('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})','').\
              str.lower().\
              str.replace('[^a-z0-9,. ]', '').\
              str.replace(r'\bamp\b', '&').\
              str.replace(r'\blt\b', '<').\
              str.replace(r'\bgt\b', '>')

    df['tweet'] = tweets
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"])
    df.to_csv("dfs/THUG_UPDATED.csv", index=False)
    return

def thug_update_two():
    df = pd.read_csv("dfs/THUG_REPLY.csv")
    reply = df['ai_reply']
    replies = []
    for r in reply:
        try:
            tmp = r.split(' ')
            i = tmp.index('\nbot')
            tmp = tmp[i+2:-1]
            rep = ' '.join(tmp)
            replies.append(rep)
        except:
            replies.append('NA')
    
    df['ai_reply'] = replies
    df.to_csv('dfs/THUG_REP_FIX.csv')
    return

def thug_final_update():
    df = pd.read_csv("dfs/THUG_FINAL.csv")
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

    # preprocessing
    months = []
    time_day = []
    for d in df['date']:
       l =  d.split(" ")
       date = l[0]
       time = l[1].split('+')[0]

       date_obj = datetime.strptime(date, '%Y-%m-%d')
       months.append(date_obj.strftime('%B'))
       time_day.append(get_time_label(time))    

    df["time_of_day"] = time_day
    df['month'] = months

    # sentiment data
    tweet_sent = []
    tweet_score = []
    reply_sent = []
    reply_score =  []
    for i in range(len(df['sentiment'])):
        x = eval(df['sentiment'][i].strip("[]"))
        x_sent = x['label']
        x_score = x['score']

        try:
            y_1 = eval(df['reply_sentiment'][i].strip("[]"))
            y_sent = y_1['label']
            y_score = y_1['score']
        except:
            y_sent = 'NA'
            y_score = 'NA'

        tweet_sent.append(x_sent)
        tweet_score.append(x_score)
        reply_sent.append(y_sent)
        reply_score.append(y_score)

    df['tweet_sent'] = tweet_sent
    df['tweet_score'] = tweet_score
    df['reply_sent'] = reply_sent
    df['reply_score'] = reply_score

    df = df.drop(columns=['sentiment', 'reply_sentiment'])
    print(df.head())

    df.to_csv("dfs/FINAL.csv", index=False)

