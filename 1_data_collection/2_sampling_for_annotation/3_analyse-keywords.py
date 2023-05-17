import pandas as pd
import glob
import os
import ast

path = os.getcwd()
csv_files = glob.glob(os.path.join(path+"\\filtered\\", "*.csv"))

subreddits = []
counts = []
inscopes = []
keywordeds = []
englishs = []
indos = []
malays = []

for name in csv_files:
    print(f"Processing {name}")
    db = pd.read_csv(name)

    scope = db["in_scope"].tolist()
    keywords = db["terms"].tolist()
    langs = db["termlangs"].tolist()
    keywords = [ast.literal_eval(i) for i in keywords]
    langs = [ast.literal_eval(i) for i in langs]

    count = 0
    inscope = 0
    keyworded = 0
    indo = 0
    english = 0
    malay = 0
    useful = []
    for i,j,k in zip(scope,keywords,langs):
        if (i == True) and len(j)>0:
            count +=1
            inscope +=1
            keyworded +=1
            useful.append(True)
        elif i == False and len(j)>0:
            keyworded +=1
            useful.append(False)
        elif i == True and len(j)==0:
            inscope +=1
            useful.append(False)
        else:
            useful.append(False)
        if "Singlish" in k:
            english +=1
        if "Indonesian" in k:
            indo +=1
        if "Malay" in k:
            malay+=1
    
    print(f"Both in-scope and keyworded: {count}")
    db["useful"] = useful
    name = name.split('\\')[-1]

    subreddits.append(name)
    counts.append(count)
    inscopes.append(inscope)
    keywordeds.append(keyworded)
    englishs.append(english)
    indos.append(indo)
    malays.append(malay)

    db.to_csv(f"./analysed/analysed_{name}",index=False)

out = pd.DataFrame(subreddits,columns=["subreddit"])
out["in-scope keyworded"] = counts
out["in-scope"] = inscopes
out["keywords"] = keywordeds
out["singlish"] = englishs
out["indo"] = indos
out["malay"] = malays
out.to_csv("stats.csv",index=False)