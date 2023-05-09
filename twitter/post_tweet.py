import json
import tweepy
import pandas as pd
import generate_tweet as gt
import os

def get_keys():
    # with open(r"C:\Users\Payton\Documents\CS325\RAPBOT\twitter\twitter_keys.json") as infile:
    #     json_obj = json.load(infile)
    #     cons_key = json_obj["api_key"]
    #     cons_sec = json_obj["api_key_secret"]
    #     acc_tok = json_obj["access_token"]
    #     acc_tok_sec = json_obj["access_token_secret"]

    cons_key = os.environ.get("CONS_KEY")
    cons_sec = os.environ.get("CONS_SEC")
    acc_tok = os.environ.get("ACC_TOK")
    acc_tok_sec = os.environ.get("ACC_TOK_SEC")

    return cons_key, cons_sec, acc_tok, acc_tok_sec

def main():
    tweet = gt.make_tweet(input=" ")

    ck, cs, at, ats = get_keys()
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs, 
                           access_token=at, access_token_secret=ats)
    
    response = client.create_tweet(text=tweet)
    print(response)
    return
