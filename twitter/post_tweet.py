import json
import tweepy
import pandas as pd

def get_keys():
    with open("twitter_keys.json") as infile:
        json_obj = json.load(infile)
        cons_key = json_obj["api_key"]
        cons_sec = json_obj["api_key_secret"]
        acc_tok = json_obj["access_token"]
        acc_tok_sec = json_obj["access_token_secret"]

        return cons_key, cons_sec, acc_tok, acc_tok_sec

def main():
    tweet = 'test tweet'

    ck, cs, at, ats = get_keys()
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs, 
                           access_token=at, access_token_secret=ats)
    #response = client.create_tweet(text=tweet)
    #print(response)

if __name__ == "__main__":
    main()