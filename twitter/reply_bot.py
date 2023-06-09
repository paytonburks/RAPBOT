import tweepy
import json
import time
import generate_tweet as gt
import pandas as pd

def get_keys():
    with open(r"C:\Users\Payton\Documents\CS325\RAPBOT\twitter\twitter_keys.json") as infile:
        json_obj = json.load(infile)
        bear_tok = json_obj["bearer_token"]
        cons_key = json_obj["api_key"]
        cons_sec = json_obj["api_key_secret"]
        acc_tok = json_obj["access_token"]
        acc_tok_sec = json_obj["access_token_secret"]

        return bear_tok, cons_key, cons_sec, acc_tok, acc_tok_sec
    
def main():
    bt, ck, cs, at, ats = get_keys()
    client = tweepy.Client(bearer_token=bt, consumer_key=ck,
                           consumer_secret=cs, access_token=at,
                           access_token_secret=ats)
    auth = tweepy.OAuth1UserHandler(consumer_key=ck,
                           consumer_secret=cs, access_token=at,
                           access_token_secret=ats)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    client_id = client.get_me().data.id

    print("Replies on")

    start_id = 1
    initialisation_resp = client.get_users_mentions(client_id)
    if initialisation_resp.data != None:
        start_id = initialisation_resp.data[0].id

    while True:
        response = client.get_users_mentions(client_id, since_id=start_id)
        if response.data != None:
            for tweet in response.data:
                try:
                    print(tweet.text)
                    # user_sent = analysis.analyze_sentiment(tweet)
                    # df = pd.DataFrame(columns=['tweet', 'sent', 'id', 'type'])
                    # row = [tweet, user_sent, response.data['id'], 'human_reply']
                    # df.loc[len(df)] = row
                    
                    inp = tweet.text[11:]
                    generated_tweet = gt.make_tweet(inp)
                    ai_resp = client.create_tweet(in_reply_to_tweet_id=tweet.id, text=generated_tweet)

                    # ai_sent = analysis.analyze_sentiment(generated_tweet)
                    # row = [generated_tweet, ai_sent, ai_resp.data['id'], 'bot_reply']
                    # df.loc[len(df)] = row
                    # df.to_csv(r'C:\Users\Payton\Documents\CS325\RAPBOT\twitter\sentiment.csv', mode='a', index=False, header=False)

                    start_id = tweet.id
                except:
                    pass

            time.sleep(60)

if __name__ == "__main__":
    main()
