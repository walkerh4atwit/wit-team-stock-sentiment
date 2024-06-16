import pandas
from alpaca.data.requests import NewsRequest
from alpaca.data.historical.news import NewsClient
import pandas as pd
from bs4 import BeautifulSoup
import time
import single_line_model


def alpaca_to_df():

    news_client = NewsClient("PKIBUX4RP07Y8PQE44Q0", "9gcVRBWDtTiiOesmUV4KXnU1osSjcvzOnGkZHsRR")
    news_request = NewsRequest(limit=50, include_content=True)
    data = news_client.get_news(news_request).dict()

    return pd.DataFrame(data['news'])


def clean(df):
    # using headline + summary instead of headline + content due to model size limitations for now
    #for i in range(len(df['content'])):
        #clean_content = BeautifulSoup(df["content"][i], "html.parser").get_text().replace("\n", "")
        #df.loc[i, 'headline'] += clean_content
    #df.drop(columns=['id', 'content', 'author', 'updated_at', 'summary', 'content', 'images', 'source'], inplace=True)
    #df.rename(columns={"headline": "headline-content"}, inplace=True)

    # headline + summary
    for i in range(len(df['headline'])):
        df.loc[i, 'headline'] += " "
        df.loc[i, 'headline'] += df.loc[i, 'summary']

    df.drop(columns=['id', 'content', 'author', 'updated_at', 'summary', 'content', 'images', 'source'], inplace=True)
    df.rename(columns={"headline": "headline-summary"}, inplace=True)

    return df


def pass_to_model(df_slice):
    single_line_model.model_function(df_slice)


# initialize most recent timestamp
most_recent_timestamp = alpaca_to_df().loc[49, 'created_at']
print(most_recent_timestamp)

# run loop calling api and results on model
while True:

    dataf = clean(alpaca_to_df())
    i = 0
    while i < 50:
        if dataf.loc[i, 'created_at'] > most_recent_timestamp:
            df_slice = dataf.loc[i]
            pass_to_model(df_slice)
            # adds line to csv
            #dataf.iloc[[i]].to_csv("temp1.csv", mode='a', header=False)
        i += 1

    most_recent_timestamp = dataf.loc[0, 'created_at']
    time.sleep(30)
