import csv
import pandas as pd
from psaw import PushshiftAPI

api = PushshiftAPI()

# Crawls comments for the given author
def author_comments_crawler(author):
    gen = api.search_comments(author=author, filter=['id', 'link_id', 'body', 'subreddit', 'author'],limit=1000)
    rows = [{'created_utc': row.created_utc, 'id': row.id, 'link_id': row.link_id, 'body': row.body, 'subreddit': row.subreddit, 'author': row.author} for row in gen]
    return rows


def num_author_comments(author):
    gen = api.search_comments(author=author, filter=['id', 'link_id', 'body', 'subreddit', 'author'])
    return api.metadata_


if __name__ == '__main__':
    author_sample = pd.read_csv("sampled_users.csv")
    author_sample = author_sample["author"].tolist()
        
    with open('output.csv', 'w',encoding="utf-8",newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['created_utc', 'id', 'link_id', 'body', 'subreddit', 'author'])
        writer.writeheader()
            
        for enum, author in enumerate(author_sample):
            print('Processing author', enum, author)
            rows = author_comments_crawler(author)
            writer.writerows(rows)
    
    print("Job done!")