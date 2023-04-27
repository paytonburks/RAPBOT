from transformers import pipeline, Conversation
import pandas as pd

def main():
    print("MAIN")
    converse = pipeline("conversational")
    print("LOADED")

    df = pd.read_csv("dfs/THUG_UPDATED.csv")
    tweets = df['tweet']

    reply = []
    for t in tweets:
        try:
            c1 = Conversation(t)
            tmp = converse([c1])
            reply.append(tmp)
        except:
            reply.append("NA")

    df['ai_reply'] = reply
    df.to_csv("dfs/THUG_REPLY.csv", index=False)

if __name__ == "__main__":
    main()
