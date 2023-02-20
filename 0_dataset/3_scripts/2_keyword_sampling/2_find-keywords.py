import pandas as pd
import re
import glob
import os

keywords = pd.read_csv("keywords.csv")
termslist = keywords["Term"].tolist()
langlistlist = keywords["Language"].tolist()


def keywordsearch(text):
    terms = []
    langs = []
    for i,j in zip(termslist,langlistlist):
        x = re.search("(?:^|\W)"+i+"(?:s\b|s\W|$|\W)",str(text),flags=re.IGNORECASE)
        if x:
            terms.append(i)
            if j not in langs:
                langs.append(j)
    return terms, langs

path = os.getcwd()
csv_files = glob.glob(os.path.join(path+"\\subreddits\\", "*.csv"))

for name in csv_files:
    print(f"Processing {name}")
    db = pd.read_csv(name)

    textlist = db["body"].tolist()
    termscolumn = []
    langscolumn = []
    for i in textlist:
        terms,langs = keywordsearch(i)
        termscolumn.append(terms)
        langscolumn.append(langs)

    db["terms"] = termscolumn
    db["termlangs"] = langscolumn
    print(db["terms"].count())
    name = name.split('\\')[-1]

    db.to_csv(f"./filtered/filetered_{name}",index=False)