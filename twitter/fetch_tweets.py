import os
from datetime import datetime, timezone, timedelta
import pandas as pd
import tweepy
import json
from google.cloud import bigquery

DATASET_ID = "thug_tweet_dataset"
TABLE_ID = "thug_tweets"

def insert_rows_to_bq(rows):
    client = bigquery.Client()
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)
    errors = client.insert_rows_json(table_ref, rows)
    if len(errors) == 0:
        print("SUCCESS")
    else:
        print(errors)

def fetch_recent_tweets_for_user(client, user_id, start_time):
    response = client.get_users_tweets(user_id, tweet_fields=["created_at"], start_time=start_time)
    # print(type(response.data[0]))
    rows = []
    if response.data is not None:
        for tweet in response.data:
            # print(tweet.created_at)
            created_at = pd.Timestamp(tweet.created_at).strftime("%Y-%m-%d %H:%M:%S")
            values = {"tweet_id": tweet.id, "author_id": user_id, "created_at": created_at, "text": tweet.text}
            rows.append(values)
    return rows

def entry_point(request): # request is a Flask request
    user_id = 238763290

    with open("twitter/twitter_keys.json") as infile:
        json_obj = json.load(infile)
        token = json_obj["bearer_token"]

    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token=token)

    start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    tweet_rows = fetch_recent_tweets_for_user(client, user_id, start_time)

    print(tweet_rows)

    if len(tweet_rows) > 0:
        insert_rows_to_bq(tweet_rows)
        
    return "Success", 200

if __name__ == "__main__":
    entry_point(None)
    