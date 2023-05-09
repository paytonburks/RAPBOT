from twitter import fetch_tweets_git as ft
from sentiment import analysis, conversation
import transform_df as trans

def main():
    print("ENTERED")
    num = ft.entry_point(None)
    if len(num) > 0:
        analysis.main()
        trans.thug_update_one()
        conversation.main()
        trans.thug_update_two()
        analysis.update()
        trans.thug_final_update()
        print("PASSED")
    return

if __name__ == "__main__":
    main()
