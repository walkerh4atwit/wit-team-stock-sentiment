import finnhub
import pandas as pd
import time

finnhub_client = finnhub.Client(api_key="cfj73ghr01que34nr220cfj73ghr01que34nr22g")


def get_finnhub_news_to_csv(finnhub_data, csv_path):
    new_data = pd.DataFrame(finnhub_data)
    current_data = pd.read_csv(csv_path)

    # current dt is the newest datetime in the existing dataset
    current_dt = current_data['datetime'][len(current_data) - 1]

    # last index in new and current dataset
    last_index_nd = len(new_data)-1
    last_index_cd = len(current_data) - 1

    # for the len of existing csv file
    for i in range(len(new_data)):
        # if the most up to date pull of the csv file is older than then current pull
        if new_data['datetime'][last_index_nd] > current_dt:
            # append that line to the last
            new_data.iloc[[last_index_cd-i]].to_csv(csv_path, mode='a', index=False, header=False)


data = finnhub_client.general_news('general', min_id=0)

get_finnhub_news_to_csv(data, 'finnhub_data.csv')

# run function every 5 minutes
#while True:
    #get_finnhub_news_to_csv(data, 'finnhub_data.csv')
    #time.sleep(300)

