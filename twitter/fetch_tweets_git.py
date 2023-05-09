import os
from datetime import datetime, timezone, timedelta
import pandas as pd
import tweepy
# from google.cloud import bigquery

# DATASET_ID = "thug_tweet_dataset"
# TABLE_ID = "thug_tweets"

# def insert_rows_to_bq(rows):
#     client = bigquery.Client()
#     dataset_ref = client.dataset(DATASET_ID)
#     table_ref = dataset_ref.table(TABLE_ID)
#     errors = client.insert_rows_json(table_ref, rows)
#     if len(errors) == 0:
#         print("SUCCESS")
#     else:
#         print(errors)

def fetch_recent_tweets_for_user(client, user_id, start_time):
    response = client.get_users_tweets(user_id, tweet_fields=["created_at", "public_metrics", "source"], start_time=start_time)
    # print(type(response.data[0]))
    rows = []
    if response.data is not None:
        # print(response.data)
        for tweet in response.data:
            # print(tweet.created_at)
            created_at = pd.Timestamp(tweet.created_at).strftime("%Y-%m-%d %H:%M:%S")
            values = {"tweet_id": tweet.id, "created_at": created_at, "text": tweet.text, "replies": tweet.public_metrics['reply_count'], "retweets": tweet.public_metrics['retweet_count'], "likes": tweet.public_metrics['like_count'], "source": tweet.source}
            rows.append(values)
    return rows

def entry_point(request): # request is a Flask request
    user_id = 238763290

    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token=bearer_token)
    client.get_users_tweets(user_id, tweet_fields=[])

    start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    tweet_rows = fetch_recent_tweets_for_user(client, user_id, start_time)
    print(tweet_rows)

    if len(tweet_rows) > 0:
        df = pd.read_csv('tweets/thugtweets.csv')
        df = df.drop(columns=['Unnamed: 0'])

        for t in tweet_rows:
            row = []
            row.extend([t['created_at']+'+00:00', t['likes'], t['replies'], t['retweets'], 'Twitter for iPhone', t['text']])
            df.loc[len(df.index)] = row
        
        df.to_csv('tweets/thugtweets.csv')

    return tweet_rows
        
entry_point(None)
