import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    df = pd.read_csv('dfs/FINAL.csv')
    
    # likes over time
    likes = df['likes']
    y = likes.to_list()
    y.reverse()
    x = [i for i in range(0, len(y))]

    dates = df['date'].to_list()
    dates.reverse()
    dates = [item[:4] for item in dates]

    plt.figure()
    plt.scatter(x, y, s=10)
    plt.title("Young Thug Likes over Time")
    plt.xlabel('Time')
    plt.ylabel('Likes')
    unique_years, year_indices = np.unique(dates, return_index=True)
    for i in range(3):
        unique_years[-(i+1)] = ""
  
    step = max(1, int(len(unique_years) / 10))
    plt.xticks(year_indices, unique_years, rotation=45, ha="right", fontsize=8)
    plt.savefig("EDA/tweets_over_time")
    plt.close()

    # grouped by tweet sentiment analysis
    grouped_sent = df.groupby("tweet_sent")

    # negative vs neutral vs positive bar chart
    x = []
    y = []
    for group, d in grouped_sent:
        x.append(group)
        y.append(len(d))

    plt.figure()
    plt.bar(x, y)
    plt.xlabel("Tweet Sentiment")
    plt.ylabel("# of Tweets")
    plt.title("Tweets by Sentiment")
    plt.close()

    grouped_sent_2017 = df.iloc[:1009].groupby("tweet_sent")
    # sentiment intensity and reply count
    plt.figure()
    col = ['r', 'b', 'g']
    i=0
    for group, d in grouped_sent_2017:
        d = d[d['replies'] > 100]
        x = d['tweet_score']
        y = d['replies']
        plt.scatter(x, y, s=10, c=col[i])
        plt.subplots_adjust(bottom=0.15)
        a, b = np.polyfit(x, y, 1)
        plt.plot(x, a*x+b, color=col[i], linestyle='--', linewidth=1)
        i+=1
    plt.title('All Sentiments')
    plt.xlabel('Sentiment Strength')
    plt.ylabel('# Replies')
    plt.savefig('eda/all_sentiment')
    plt.close()

    i=0
    for group, d in grouped_sent_2017:
        d = d[d['replies'] > 100]
        x = d['tweet_score']
        y = d['replies']
        plt.figure()
        plt.scatter(x, y, s=10, c=col[i])
        plt.subplots_adjust(bottom=0.15)
        a, b = np.polyfit(x, y, 1)
        plt.plot(x, a*x+b, color=col[i], linestyle='--', linewidth=1)
        # plt.text(0.5, 0.8, , size=12, va='top')
        plt.title('y = ' + '{:.2f}'.format(b) + ' {:.2f}'.format(a) + 'x')
        plt.xlabel('Sentiment Strength')
        plt.ylabel('# Replies')
        plt.savefig('eda/'+group+' replies')
        plt.close()
        i+=1

    return


if __name__ == "__main__":
    main()
