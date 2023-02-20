import datetime as dt
import pandas as pd
from datetime import datetime

from psaw import PushshiftAPI

api = PushshiftAPI()


def readutc(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.date()

def crawl_all_posts(subreddit):
    gen = api.search_submissions(subreddit=subreddit, filter=['id', 'created_utc', 'title', 'selftext', 'author', 'score', 'num_comments', 'num_crossposts'])
    return gen

def crawl_all_comments(subreddit):
    #start_time_epoch = int(dt.datetime(year=2021, month=8, day=1, hour=0, minute=0).timestamp())
    end_time_epoch = int(dt.datetime(year=2022, month=8, day=31, hour=23, minute=59).timestamp())
    
    #gen = api.search_comments(subreddit=subreddit, after=start_time_epoch, before=end_time_epoch, filter=['id', 'link_id', 'parent_id', 'body', 'author'])
    gen = api.search_comments(subreddit=subreddit, before=end_time_epoch, filter=['id', 'link_id', 'parent_id', 'body', 'author'])
    return gen


if __name__ == '__main__':
    subreddits = pd.read_csv("subreddits.csv")["subreddit"].tolist()
    total_entries = 0
    entries = []
    first_comment = []
    last_comment = []
    
    for sr in subreddits:
        print(f"Pulling from {sr}.")
        #gen = crawl_all_posts(sr)
        gen = crawl_all_comments(sr)
        data = []

        for row in gen:
            #data.append({'id':row.id, 'date':row.created_utc, 'title':row.title, 'selftext':row.selftext, 'author':row.author, 'score':row.score, 'num_comments':row.num_comments, 'num_crossposts':row.num_crossposts})
            data.append({'created_utc':row.created_utc, 'id':row.id, 'link_id':row.link_id, 'parent_id':row.parent_id, 'body':row.body, 'author':row.author})
            print(f"Processed so far: {len(data)} entries.\r")
        
        results_df = pd.DataFrame(data)
        results_df["date"] = results_df["created_utc"].apply(readutc)
        entries.append(len(results_df))
        first_comment.append(min(results_df["date"]))
        last_comment.append(max(results_df["date"]))

        results_df.to_csv(f'./data/{sr}.csv', index=False)
        print(f'Exported to ./data/{sr}.csv')
        total_entries+=len(data)
        print(f'Total entries so far: {total_entries}.')
    
    print(f"Total entries across subreddits: {total_entries}.")

    stats = pd.DataFrame(subreddits,columns=["subreddit"])
    stats["entries"] = entries
    stats["first_comment"] = first_comment
    stats["last_comment"] = last_comment
    stats.to_csv("subreddit_stats.csv",index=False)
    print("Stats written to subreddit_stats.csv")
