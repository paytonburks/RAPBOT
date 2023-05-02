"""
predict tweet reply sentiment
predict likes
predict 
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from datetime import datetime
import random


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


def main():    
    random.seed(10)
    # read in data
    df = pd.read_csv("dfs/THUG_FINAL.csv")
    df = df[df.reply_sentiment.notnull()]
    df = df.reset_index()
    # base input and output data
    y = df['reply_sentiment']
    X = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'ai_reply', 'reply_sentiment', 'index'])

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

    X["time_of_day"] = time_day
    X['month'] = months

    X = X.drop(columns=["date"])

    # sentiment data
    tweet_sent = []
    tweet_score = []
    reply_sent = []
    reply_score =  []
    y_na_ind = []
    for i in range(len(X['sentiment'])):
        x = eval(X['sentiment'][i].strip("[]"))
        x_sent = x['label']
        x_score = x['score']

        try:
            y_1 = eval(y[i].strip("[]"))
            y_sent = y_1['label']
            y_score = y_1['score']
        except:
            y_sent = 'NA'
            y_score = 'NA'
            y_na_ind.append(i)

        tweet_sent.append(x_sent)
        tweet_score.append(x_score)
        reply_sent.append(y_sent)
        reply_score.append(y_score)

    X['tweet_sent'] = tweet_sent
    X['tweet_score'] = tweet_score
    X = X.drop(['tweet', 'sentiment'], axis=1)

    # what we want to predict
    y = reply_sent

    # convert categorical to numerical
    le = preprocessing.LabelEncoder()
    cat_cols = ['source', 'time_of_day', 'month', 'tweet_sent']
    for col in cat_cols:
        X[col] = le.fit_transform(X[col])

    # fitting the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    # prediction time
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    return


if __name__ == "__main__":
    main()
