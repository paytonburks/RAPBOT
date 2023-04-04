import snscrape.modules.twitter as sntwitter
import pandas as pd

attributes_container = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:youngthug').get_items()):
    if i>10000:
        break
    attributes_container.append([tweet.date, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.sourceLabel, tweet.content,])

tweets_df = pd.DataFrame(attributes_container, columns=["date", "likes", "replies", "retweets", "source", "tweet"])
tweets_df.to_csv('tweets/youngthugtweets.csv')
