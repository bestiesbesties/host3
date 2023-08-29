import requests
import json
import pandas as pd
from datetime import datetime

with open('/home/leytonserver/host/host3/config.json') as config_file:
    config = json.load(config_file)

output_string = config["name"].replace(" ", "").lower()
filepath_google = f'/home/leytonserver/host/data/googleapi_data_{output_string}.csv'

def get2(place_name):
    api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place_name,
        "inputtype": "textquery",
        "fields": "name,rating,user_ratings_total",
        "key": config["google"]
    }

    response = requests.get(api_url, params=params)
    data = json.loads(response.text)
    candidates = data.get("candidates", [])
    business_data = candidates[0]
    reviews_count = business_data.get("user_ratings_total", 0)
    return {'reviews':reviews_count}

def update_dataframe2(c1):
    print(c1,str(datetime.now()).split('.')[0][:-3])
    data = pd.read_csv(filepath_google, sep=',', index_col=0)
    total = c1['reviews']
    timestamp = str(datetime.now()).split('.')[0]
    if data.empty or total != data['count'].iloc[-1]:
        new_row = {'count': total, 
                    'timestamp':timestamp
                    }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(filepath_google)
    return data
update_dataframe2(get2(config["name"]))