import pandas as pd
import ast
import glob
import os
import re

path = os.getcwd()
csv_files = glob.glob(os.path.join(path+"\\analysed\\", "*.csv"))

totaldb = []

for name in csv_files:
    print(f"Processing {name}")
    db = pd.read_csv(name)
    db = db[~(db["useful"] == False)]
    totaldb.append(db)

totaldb = pd.concat(totaldb)

print(totaldb)
totaldb = totaldb.drop_duplicates("body")

pastdb = pd.read_csv("singapore_batch_1-2.csv")
print(len(totaldb))
bodylist = pastdb["body"].tolist()
totaldb = totaldb[~(totaldb["body"].isin(bodylist))]
print(len(totaldb))

keywords = totaldb["terms"].tolist()
keywords = [ast.literal_eval(i) for i in keywords]
#print(keywords)
newkeywords = []
for i in keywords:
    #print(i)
    i.sort()
    #print(i)
    newkeywords.append(str(i))

totaldb["terms"] = newkeywords

keywordlist = pd.read_csv("keywords.csv")["Term"].tolist()
SAMPLE_SIZE = 15

sample_df = totaldb.copy()
exclude_word = ""
results = []
for k in keywordlist:
    print(k)
    print(sample_df[sample_df.terms.str.contains(k)].size)
    if exclude_word != "":
        sample_df = sample_df[~sample_df.terms.str.contains(exclude_word)]
    if sample_df[sample_df.terms.str.contains(k)].size > 0:
        count = sample_df[sample_df.terms.str.contains(k)].size
        results.append(sample_df[sample_df.terms.str.contains(k)].sample(min(count,SAMPLE_SIZE),replace=True))
    exclude_word=k

result_df = pd.concat(results)

def urlscript(text):
    out = re.sub(r"http\S+",'[URL]',text)
    return out
result_df["body"] = result_df["body"].apply(urlscript)

def truncatescript(text):
    out = text[:500]
    return out
result_df["body"] = result_df["body"].apply(truncatescript)

result_df = result_df.drop_duplicates("body")

print(result_df)

shuffleddb = result_df.sample(frac=1).reset_index(drop=True)
shuffleddb = shuffleddb.sample(2000)
print(shuffleddb)
shuffleddb.to_csv("singapore_batch_2.csv", index=False)

