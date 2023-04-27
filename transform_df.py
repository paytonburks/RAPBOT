import pandas as pd
import re


def thug_update_one():
    df = pd.read_csv("dfs/THUG_SENT_DF.csv")
    tweets = df['tweet'].\
              str.replace('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})','').\
              str.lower().\
              str.replace('[^a-z0-9,. ]', '').\
              str.replace(r'\bamp\b', '&').\
              str.replace(r'\blt\b', '<').\
              str.replace(r'\bgt\b', '>')

    df['tweet'] = tweets
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"])
    df.to_csv("dfs/THUG_UPDATED.csv", index=False)
    return

def thug_update_two():
    df = pd.read_csv("dfs/THUG_REPLY.csv")
    reply = df['ai_reply']
    replies = []
    for r in reply:
        try:
            tmp = r.split(' ')
            i = tmp.index('\nbot')
            tmp = tmp[i+2:-1]
            rep = ' '.join(tmp)
            replies.append(rep)
        except:
            replies.append('NA')
    
    df['ai_reply'] = replies
    df.to_csv('dfs/THUG_REP_FIX.csv')
    return

if __name__ == "__main__":
    thug_update_two()
