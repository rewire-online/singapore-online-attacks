import pandas as pd
from datetime import datetime
import time

data = pd.read_csv("SingaporeRaw_comments_all.csv")

def readutc(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.date()

data["date"] = data["created_utc"].apply(readutc) #read dates from UTC timestamps

data = data[~(data["date"] < datetime(2021,8,1).date())] #remove before 1st August 2021
data = data[~(data["date"] > datetime(2022,8,31).date())] #remove after 31st August 2022
data = data[~(data["author"] == "[deleted]")] #remove posts by banned users
print(data)

sampled_users = data["author"].sample(1000)
print(sampled_users)
sampled_users.to_csv("sampled_users.csv", index=False)

most_active = data['author'].value_counts()[:1000].index.tolist()
posts = data['author'].value_counts()[:1000].tolist()
activedata = pd.DataFrame(most_active,columns=["author"])
activedata["comment_count"] = posts
activedata.to_csv("active_users.csv",index=False)
print(activedata)
