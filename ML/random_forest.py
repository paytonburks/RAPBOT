"""
predict tweet reply sentiment
predict likes
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
    df = pd.read_csv("dfs/FINAL.csv")
    df = df[df.reply_sent.notnull()]
    df = df.reset_index()
    
    # base input and output data
    y = df['reply_sent']
    X = df.drop(columns=['reply_score', 'reply_sent', 'date', 'tweet', 'ai_reply', 'index'])
    
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
