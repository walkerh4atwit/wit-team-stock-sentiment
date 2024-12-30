from alpaca.data.live import NewsDataStream
from alpaca.data.models.news import News
from transformers import BertForSequenceClassification, BertTokenizer
from oracledb.exceptions import ProgrammingError as OracleProgrammingError

import traceback
import os, torch
import model_loader
import database_push
from db_connect import db_connect
from transformers import logging as trf_logging

trf_logging.set_verbosity_error()

# gets the most recent 50 articles
# def alpaca_to_df():
#     news_client = NewsClient("key", "secret_key")
#     news_request = NewsRequest(limit=50)
#     data = news_client.get_news(news_request).dict()

#     return pd.DataFrame(data['news'])

articles_nextval_query = """
    SELECT articles_seq.NEXTVAL FROM dual
    """

tickers_nextval_query = """
    SELECT tickers_seq.NEXTVAL FROM dual
    """

post_article_query = """
    INSERT INTO Articles (id, title, url, summary, date_published)
    VALUES (:1, :2, :3, :4, TO_TIMESTAMP(:5, 'YYYY-MM-DD"T"HH24:MI:SS"Z"'))
    """

post_ticker_query = """
    INSERT INTO Tickers (id, ticker)
    VALUES (:1, :2)
    """

get_ticker_id_query = """
    SELECT id FROM Tickers WHERE ticker = :1
    """

get_sector_id_of_ticker_query = """
    SELECT sector_id FROM Tickers WHERE id = :1
    """

post_articleticker_query = """
    INSERT INTO Articletickers (article_id, ticker_id, sentiment_score)
    VALUES (:1, :2, :3)
    """

update_ticker_score_query = """
    UPDATE Tickers 
    SET sentiment_score = 
        (SELECT AVG(sentiment_score) 
        FROM Articletickers
        WHERE id = :1)
    WHERE id = :1
    """

update_sector_score_query = """
    UPDATE Sectors 
    SET sentiment_score =
        (SELECT AVG(sentiment_score)
        FROM 
            (SELECT id AS ticker_id, sector_id
            FROM Tickers WHERE sector_id = :1) T_subquery
        INNER JOIN Articletickers 
        ON T_subquery.ticker_id = Articletickers.ticker_id)
    WHERE id = :1
    """

def find_api_keys() -> tuple[str]:
    api_key = os.environ.get("API_KEY")
    api_secret_key = os.environ.get("API_SECRET_KEY")
    return api_key, api_secret_key

def push_article(headline, url, summary, date_published):
    database_push.push_article(headline, url, summary, date_published)   

def pass_to_model(text, symbols, url):
    model_loader.model_function(text, symbols, url)

async def socket_handler(data: News):
    tokens = ml_tokenizer.encode(data.headline, return_tensors='pt')
    result = ml_model(tokens)
    score = torch.argmax(result.logits).item()

    # db connection
    cnx = db_connect()
    csr = cnx.cursor()

    # gets next number from sequence
    csr.execute(articles_nextval_query)
    article_id = csr.fetchone()[0]

    if data.symbols:
        # pushes the article info to the db on oci
        csr.execute(post_article_query, (article_id, data.headline, data.url, data.summary, data.created_at))

    try:
        for symbol in data.symbols:
            # grabs the ticker id for the ticker
            csr.execute(get_ticker_id_query, (symbol,))
            ticker_id = csr.fetchone()[0]

            #
            if ticker_id is None:
                csr.execute(tickers_nextval_query)
                ticker_id = csr.fetchone()[0]

                csr.execute(post_ticker_query, (ticker_id, symbol))

            if ticker_id is None:
                raise Exception("Ticker ID not generated! Aborting worker thread.")

            csr.execute(post_articleticker_query, (article_id, ticker_id, score))
            csr.execute(update_ticker_score_query, (ticker_id,))

            csr.execute(get_sector_id_of_ticker_query, (ticker_id,))
            sector_id = csr.fetchone()[0]

            if sector_id is not None:
                csr.execute(update_sector_score_query, (sector_id,))

    except OracleProgrammingError as e:
        print("Data symbols:",data.symbols)
        print("Data:",data)
        print(e)
        traceback.print_exc()
        
    cnx.commit()



# call api and results on model
# dataf = alpaca_to_df()
# i = 0

# while i < 50:
#     row = dataf.iloc[i]

#     push_article(dataf.loc[i, "headline"], dataf.loc[i, "url"], dataf.loc[i, "summary"], dataf.loc[i, 'created_at'])
#     pass_to_model((dataf.loc[i, "headline"]), dataf.loc[i, 'symbols'], dataf.loc[i, 'url'])
#     i += 1

# if datetime.now().hour == 0 and datetime.now().minute == 0:
#     database_push.delete_old_articles()

api_key, api_secret_key = find_api_keys()

ml_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
ml_model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
ml_model.load_state_dict(torch.load('/var/lib/sentiments/ml_model.pth', map_location=torch.device('cpu')))

data_stream = NewsDataStream(api_key=api_key, secret_key=api_secret_key)
data_stream.subscribe_news(socket_handler, "*")

data_stream.run()