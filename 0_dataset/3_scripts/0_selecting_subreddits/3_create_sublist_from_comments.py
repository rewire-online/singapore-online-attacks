import pandas as pd

data = pd.read_csv("output-sampled.csv")
subreddits = data["subreddit"]
subreddits = subreddits.drop_duplicates()
subreddits.to_csv("subreddits-sampled.csv",index=False)