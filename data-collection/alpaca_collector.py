from alpaca.data.requests import NewsRequest
from alpaca.data.historical.news import NewsClient
import pandas as pd
import time
import model_load_test
import database_push
from datetime import datetime
from transformers import logging

logging.set_verbosity_error()


def alpaca_to_df():

    news_client = NewsClient("key", "secret_key")
    news_request = NewsRequest(limit=50)
    data = news_client.get_news(news_request).dict()

    return pd.DataFrame(data['news'])


def pass_to_model(text, symbols, url):
    model_load_test.model_function(text, symbols, url)


# initialize most recent timestamp
most_recent_timestamp = alpaca_to_df().loc[49, 'created_at']
print(most_recent_timestamp)

# run loop calling api and results on model
while True:

    dataf = alpaca_to_df()
    i = 0
    while i < 50:
        if dataf.loc[i, 'created_at'] > most_recent_timestamp:
            database_push.push_article(dataf.loc[i, "headline"], dataf.loc[i, "url"], dataf.loc[i, "summary"], dataf.loc[i, 'created_at'])
            pass_to_model((dataf.loc[i, "headline"]), dataf.loc[i, 'symbols'], dataf.loc[i, 'url'])

        i += 1

    most_recent_timestamp = dataf.loc[0, 'created_at']
    if datetime.now().hour == 0 and datetime.now().minute == 0:
        database_push.delete_old_articles()
    time.sleep(30)
