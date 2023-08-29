import requests
import json
import pandas as pd
from datetime import datetime

with open('/home/leytonserver/host/host3/config.json') as config_file:
    config = json.load(config_file)

output_string = config["name"].replace(" ", "").lower()
filepath_short = f'/home/leytonserver/host/data/shortapi_data_{output_string}.csv'

def get(linkID):
    if linkID != "None":
        APIKEY = config["short"]
        url = f'https://api-v2.short.io/statistics/link/{linkID}'
        querystring = {
            "period": "total",
            "tzOffset": "0"
        }
        headers = {
            'accept': "*/*",
            'authorization': APIKEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text) 
        
        score_human = data["humanClicks"]

        score_ios = 0
        for os_item in data["os"]:
            if os_item["os"] == "iOS":
                score_ios = os_item["score"]
                break

        score_android = 0
        for os_item in data["os"]:
            if os_item["os"] == "Android":
                score_android = os_item["score"]
                break
    else:
        score_human = 0
        score_ios = 0
        score_android = 0
    
    return {'human': score_human, 'iOS': score_ios, 'Android': score_android}


def update_dataframe(c1, c2, c3):
    print(c1, c2, c3, str(datetime.now()).split('.')[0][:-3])
    data = pd.read_csv(filepath_short, sep=',', index_col=0, dtype={'count': int})

    if config["kaart3"] != None:
        total = c1['human'] + c2['human'] + c3['human']
        timestamp = str(datetime.now()).split('.')[0]
        if data.empty or total > data['count'].iloc[-1]:
            new_row = {'count': total,
                       'c1_human': int(c1["human"]),
                       'c1_ios': int(c1["iOS"]),
                       'c1_android': int(c1["Android"]),
                       'c2_human': int(c2["human"]),
                       'c2_ios': int(c2["iOS"]),
                       'c2_android': int(c2["Android"]),
                       'c3_human': int(c3["human"]),
                       'c3_ios': int(c3["iOS"]),
                       'c3_android': int(c3["Android"]),
                       'timestamp': timestamp
                       }
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            data.to_csv(filepath_short)

    return data

update_dataframe(get(config["kaart1"]),
                get(config["kaart2"]),
                get(config["kaart3"])
                )