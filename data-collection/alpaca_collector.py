from alpaca.data.requests import NewsRequest
from alpaca.data.historical.news import NewsClient
import pandas as pd
import time
import model_load_test


def alpaca_to_df():

    news_client = NewsClient("PKIBUX4RP07Y8PQE44Q0", "9gcVRBWDtTiiOesmUV4KXnU1osSjcvzOnGkZHsRR")
    news_request = NewsRequest(limit=50)
    data = news_client.get_news(news_request).dict()

    return pd.DataFrame(data['news'])


def clean(df):

    for i in range(len(df['headline'])):

        clean_summary = " ".join(df.loc[i, "summary"].split())
        df.loc[i, "summary"] = clean_summary
        clean_summary = clean_summary.replace('&#39;', '\'')

        df.loc[i, 'headline'] += " | "
        df.loc[i, 'headline'] += clean_summary

    df.drop(columns=['id', 'content', 'author', 'updated_at', 'summary', 'images', 'source'], inplace=True)
    df.rename(columns={"headline": "headline-summary"}, inplace=True)

    return df


def pass_to_model(df_slice, col):
    model_load_test.model_function(df_slice, col)


DF_COL = 'headline-summary'

# initialize most recent timestamp
most_recent_timestamp = alpaca_to_df().loc[49, 'created_at']
print(most_recent_timestamp)

# run loop calling api and results on model
while True:

    dataf = clean(alpaca_to_df())
    i = 0
    while i < 50:
        if dataf.loc[i, 'created_at'] > most_recent_timestamp:
            pass_to_model(dataf.loc[i], DF_COL)
        i += 1

    most_recent_timestamp = dataf.loc[0, 'created_at']
    time.sleep(30)
