import pandas as pd
import ast
import os
from collections import Counter

path = os.getcwd()
csv_files = ["singapore_batch_2.csv"]

allkeywords = []
for name in csv_files:
    print(f"Processing {name}")
    db = pd.read_csv(name)

    keywords = db["terms"].tolist()
    keywords = [ast.literal_eval(i) for i in keywords]

    for i in keywords:
        for j in i:
            allkeywords.append(j)
    #print(allkeywords)

keys = Counter(allkeywords).keys()
values = Counter(allkeywords).values()
out = pd.DataFrame(keys,columns=["Term"])
out["count"] = values

out.to_csv("termstats-2.csv",index=False)