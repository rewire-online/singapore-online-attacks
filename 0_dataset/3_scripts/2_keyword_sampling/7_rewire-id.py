import pandas as pd

db = pd.read_csv("singapore_batch_2-translated.csv")
db["batch"] = "batch_2"
ids = []
count = 800
for i in db["body"].tolist():
    ids.append(f"singapore_{count}")
    count+=1
db["rewire_id"] = ids

db.to_csv("singapore_batch_2-translated.csv",index=False)