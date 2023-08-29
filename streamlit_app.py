import streamlit as st
import pandas as pd
from datetime import timedelta
import json


with open('config.json') as config_file:
    config = json.load(config_file)

output_string = config["name"].replace(" ", "").lower()

# page settings
st.set_page_config(
    page_title="Boostercard analytics",
    page_icon=":bar_chart:",
    layout='wide',
)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

font_link = '<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">'
st.markdown(font_link, unsafe_allow_html=True)

# data
scan_data = pd.read_csv(f'http://95.99.70.232:8000/shortapi_data_{output_string}.csv', sep=',', index_col=0)
# Convert timestamp strings to datetime objects
scan_data['timestamp'] = pd.to_datetime(scan_data['timestamp'])
scans = scan_data.iloc[-1]

review_data = pd.read_csv(f'http://95.99.70.232:8000/googleapi_data_{output_string}.csv', sep=',', index_col=0)
# Convert timestamp strings to datetime objects
review_data['timestamp'] = pd.to_datetime(review_data['timestamp'])
reviews = review_data.iloc[-1]

# Verify review integrity via saved logs
pre_scans_data = scan_data[['count', 'timestamp']]
result_data = []

for _, scan_row in pre_scans_data.iterrows():
    scan_timestamp = scan_row['timestamp']
    valid_passes = review_data[
        (review_data['timestamp'] >= scan_timestamp - timedelta(minutes=5)) &
        (review_data['timestamp'] <= scan_timestamp + timedelta(minutes=30))
    ]

    if not valid_passes.empty:
        for _, pass_row in valid_passes.iterrows():
            if pass_row['timestamp'] > scan_row['timestamp']:
                time_difference = pass_row['timestamp'] - scan_row['timestamp']
            else:
                time_difference = scan_row['timestamp'] - pass_row['timestamp']
            result_data.append({
                'scan_count': scan_row['count'],
                'review_count': pass_row['count'],
                'scan_timestamp': scan_row['timestamp'],
                'review_timestamp': pass_row['timestamp'],
                'time_difference': time_difference
            })
        result_df = pd.DataFrame(result_data)
    else:
        result_df = pd.DataFrame(columns=['scan_count',
                                          'review_count',
                                          'scan_timestamp',
                                          'review_timestamp',
                                          'time_difference'
                                          ])

st.title(f'Hi, {config["name"]}!')
# row a
totals = scans['count']
a1, a2 = st.columns(2)
a1.metric(f"Totaal aantal scans", totals)
a2.metric("Aantal reviews door Boostercards ", result_df.shape[0] ,int(reviews['count']))

st.markdown("---")

# row b
b1, b2, b3, b4, b5, b6 = st.columns(6)

with b1:
    st.image('images/boostercard.png')
with b2:
    name = "Boostercard 1"
    st.metric(f"{name}", f"{int(scans['c1_human'])}")
    st.write(f"{'Scan' if int(scans['c1_human']) == 1 else 'Scans'}")
with b3:
    st.image('images/boostercard.png')
with b4:
    name = "Boostercard 2"
    st.metric(f"{name}", f"{int(scans['c2_human'])}")
    st.write(f"{'Scan' if int(scans['c2_human']) == 1 else 'Scans'}")
# with b5:
#     st.image('images/boostercard.png')
# with b6:
#     name = "Boostercard 3"
#     st.metric(f"{name}", f"{int(scans['c3_human'])}")
#     st.write(f"{'Scan' if int(scans['c3_human']) == 1 else 'Scans'}")

# c1, c2, c3 = st.columns((2,1,1))
# with c1:
#     if not result_df.empty:
#         time_columns = ['scan_timestamp', 'review_timestamp', 'time_difference']
#         result_df[time_columns] = result_df[time_columns].astype(str)
#         c1.dataframe(result_df)
#     else:
#         c1.write("Nog géén reviews achtergelaten door Boostercards.")
# with c2:
#     c2.dataframe(scan_data[['count','timestamp']])
# with c3:
#     c3.dataframe(review_data )

# hide options
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
