from alpaca.data.requests import NewsRequest
from alpaca.data.historical.news import NewsClient
import pandas as pd
from bs4 import BeautifulSoup


def clean_to_csv(df):
    for i in range(len(df['content'])):
        clean_content = " ".join(BeautifulSoup(df.loc[i, "content"], "html.parser").get_text().split())
        df.loc[i, 'content'] = clean_content

        clean_summary = " ".join(df.loc[i, "summary"].split())
        df.loc[i, "summary"] = clean_summary

    prefix = str(df.loc[0, 'created_at'])[:10]
    df.to_csv(r"C:\Users\hp\Dev\data\\" + prefix + "data.csv")


def extendable_alpaca(data_list_, page_token):
    news_client = NewsClient("PKIBUX4RP07Y8PQE44Q0", "9gcVRBWDtTiiOesmUV4KXnU1osSjcvzOnGkZHsRR")
    news_request = NewsRequest(page_token=page_token, limit=50, include_content=True)
    data = news_client.get_news(news_request).dict()
    data_list_.extend(data['news'])

    return data['next_page_token']


counter = 0
token = None
while True:
    data_list = []
    for i in range(200):
        token = extendable_alpaca(data_list, token)

    clean_to_csv(pd.DataFrame(data_list))
    counter += 1
    print(counter)
