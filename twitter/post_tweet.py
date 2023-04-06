import json
import tweepy
import pandas as pd
import generate_tweet as gt

def get_keys():
    with open(r"C:\Users\Payton\Documents\CS325\RAPBOT\twitter\twitter_keys.json") as infile:
        json_obj = json.load(infile)
        cons_key = json_obj["api_key"]
        cons_sec = json_obj["api_key_secret"]
        acc_tok = json_obj["access_token"]
        acc_tok_sec = json_obj["access_token_secret"]

        return cons_key, cons_sec, acc_tok, acc_tok_sec

def main():
    tweet = gt.make_tweet(input=" ")
    print(tweet)

    ck, cs, at, ats = get_keys()
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs, 
                           access_token=at, access_token_secret=ats)
    
    inp = input("Do you want to post this tweet? Type Y: ")
    if inp == "Y":
        response = client.create_tweet(text=tweet)
        print(response)
    elif inp == "E":
        edited = input("Edited tweet: ")
        response = client.create_tweet(text=edited)
    else:
        return


    
if __name__ == "__main__":
    main()