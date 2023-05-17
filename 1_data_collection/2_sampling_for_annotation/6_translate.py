import pandas as pd
import requests
import json

deepl_url = 'https://api.deepl.com/v2/translate'

with open("key") as f:
    deepl_auth_key = json.load(f)['key']

def trans_deepl(text, target_lang):
    
    payload = {"target_lang": target_lang, "auth_key": deepl_auth_key, "text": text}
    response = requests.post(url = deepl_url, data = payload)
    
    for translation in response.json()["translations"]:
        trans_text = translation["text"]   
    
    return trans_text

db = pd.read_csv("singapore_batch_2.csv")

TARGET_LANG = "en"

db["trans_deepl"] = db.body.apply(lambda x: trans_deepl(x, TARGET_LANG))

db.to_csv("singapore_batch_2-translated.csv",index=False)