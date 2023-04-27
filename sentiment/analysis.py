from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def main():
    print('MAIN')
    thug_df = pd.read_csv('tweets/thugtweets.csv')
    tweets = thug_df['tweet']
    t_sentiment = []

    print("BEGINNING SENTIMENT")
    for t in tweets:
        t_sentiment.append(classifier(t))    

    print("TIDYING UP") 
    thug_df['sentiment'] = t_sentiment
    thug_df.to_csv("dfs/THUG_SENT_DF.csv")
    
    return

def update():
    print("UPDATE")
    df = pd.read_csv('dfs/THUG_REP_FIX.csv')
    reps = df['ai_reply']
    r_sentiment = []

    print("BEGINNING SENTIMENT")
    for r in reps:
        try:
            r_sentiment.append(classifier(r))
        except:
            r_sentiment.append("NA")

    print("TIDYING UP") 
    df['reply_sentiment'] = r_sentiment
    df.to_csv("dfs/THUG_FINAL.csv")

if __name__ == "__main__":
    update()

