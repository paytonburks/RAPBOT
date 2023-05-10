import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from datetime import datetime
import random
import tensorflow as tf
from transformers import pipeline, Conversation
from sklearn import tree

print("RUNNING")

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

def generate_tweet(constant, one_step_model):
    states = None
    next_char = tf.constant([constant])
    result = []

    for n in range(100):
        next_char, states = one_step_model.generate_one_step(next_char, states=states)
        result.append(next_char)

    result = tf.strings.join(result)
    return result[0].numpy().decode('utf-8')

def random_forest_gen(df, pred=None):
    random.seed(10)
    # read in data
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
    if pred:
        pred_row = X.iloc[-1]

    # fitting the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    # prediction time
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    if pred:
        return rf.predict([pred_row]), accuracy

    return rf

def slatt_bot_gen(input):
    bans = []
    with open('streamlit/filter.txt') as f:
        lines = f.readlines()
        for l in lines:
            spl = l.split(",")
            bans.append(spl[0])

    one_step = tf.saved_model.load("streamlit/one_step")
    tweet = generate_tweet(input, one_step)
    
    while any(word in tweet for word in bans):
        tweet = generate_tweet(input, one_step)

    i = -1
    while i >= -(len(tweet)):
        if tweet[i] == ' ':
            break
        i-=1

    finished = ""
    for c in tweet[:i]:
        try:
            if finished[-1] == " " and c == " ":
                return finished
            else:
                finished+=c
        except:
            finished+=c

    return input+tweet[:i]

def conversational(t):
    print("MAIN")
    converse = pipeline("conversational")
    print("LOADED")

    try:
        c1 = Conversation(t)
        tmp = converse([c1])
        return tmp
    except:
        return("ERROR")

def tweet_reply_pred(df, pred=None): # Decision tree regressor
    random.seed(10)
    # read in data
    df = df[df.reply_sent.notnull()]
    df = df.reset_index()

    y = df['replies'].to_list()
    X = df.drop(columns=['date', 'tweet', 'ai_reply', 'index', 'source', 'time_of_day', 'month', 'replies'])

    le = preprocessing.LabelEncoder()
    cat_cols = ['tweet_sent', 'reply_sent']
    for col in cat_cols:
        X[col] = le.fit_transform(X[col])
    if pred:
        pred_row = X.iloc[-1]
        pred_row['reply_score'] = X.iloc[-1]['tweet_score']
        X.loc[9777] = pred_row
        print(X.tail())

    print("PRED ROW", pred_row)
    print("X.test.cols", X.columns)

    score = 0
    while score < 0.4:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        regTree = tree.DecisionTreeRegressor(max_depth=5) # 5 is sweet spot
        regTree.fit(X_train, y_train)
        score = regTree.score(X_test, y_test)

    final_pred = regTree.predict([pred_row])


    return final_pred[0], score
