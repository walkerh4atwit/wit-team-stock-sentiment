from alpaca.data.requests import NewsRequest
from alpaca.data.historical.news import NewsClient
import pandas as pd
import model_loader
import database_push
from datetime import datetime
from transformers import logging

logging.set_verbosity_error()

# gets the most recent 50 articles
def alpaca_to_df():
    news_client = NewsClient("key", "secret_key")
    news_request = NewsRequest(limit=50)
    data = news_client.get_news(news_request).dict()

    return pd.DataFrame(data['news'])

def push_article(headline, url, summary, date_published):
    database_push.push_article(headline, url, summary, date_published)   

def pass_to_model(text, symbols, url):
    model_loader.model_function(text, symbols, url)

# call api and results on model
dataf = alpaca_to_df()
i = 0

while i < 50:
    row = dataf.iloc[i]

    push_article(dataf.loc[i, "headline"], dataf.loc[i, "url"], dataf.loc[i, "summary"], dataf.loc[i, 'created_at'])
    pass_to_model((dataf.loc[i, "headline"]), dataf.loc[i, 'symbols'], dataf.loc[i, 'url'])
    i += 1

if datetime.now().hour == 0 and datetime.now().minute == 0:
    database_push.delete_old_articles()