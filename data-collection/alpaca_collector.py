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

articles_nextval_query = """
    SELECT articles_seq.NEXTVAL FROM dual
    """

tickers_nextval_query = """
    SELECT tickers_seq.NEXTVAL FROM dual
    """

post_article_query = """
    INSERT INTO Articles (id, title, url, summary, date_published)
    VALUES (:1, :2, :3, :4, TO_TIMESTAMP_TZ(:5, 'YYYY-MM-DD HH24:MI:SS TZH:TZM'))
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
    # passing data through the ml model
    tokens = ml_tokenizer.encode(data.headline, return_tensors='pt')
    result = ml_model(tokens)
    score = torch.argmax(result.logits).item()

    # db connection
    cnx = db_connect()
    csr = cnx.cursor()

    # gets next number from sequence
    csr.execute(articles_nextval_query)
    article_id_result = csr.fetchone()

    # if there is some issue with the sequence...
    if article_id_result is None:
        raise Exception("Article ID not generated or found! Aborting worker thread.")

    article_id = article_id_result[0]

    # 
    if data.symbols:
        # pushes the article info to the db on oci
        csr.execute(post_article_query, (article_id, data.headline, data.url, data.summary, data.created_at.strftime("%Y-%m-%d %H:%M:%S%z")))
    else:
        print("Article has no symbols... printing data")
        print("All data:", data)
        print("The prospective score:", score)

    # try-catch to debug some stuff
    try:
        # loop through symbols mentioned in article
        for symbol in data.symbols:

            # grabs the ticker id for the ticker
            csr.execute(get_ticker_id_query, (symbol,))
            existing_ticker_id_result = csr.fetchone()

            # adding a ticker to the db
            if existing_ticker_id_result is None:
                # find the next greatest value in the sequence
                csr.execute(tickers_nextval_query)
                new_ticker_id_result = csr.fetchone()

                if new_ticker_id_result is None:
                    raise Exception("Ticker ID not generated or found! Aborting worker thread.")

                csr.execute(post_ticker_query, (new_ticker_id_result[0], symbol))

                existing_ticker_id_result = new_ticker_id_result
            
            # takes the id from the existing match for the symbol
            # whether or not I just created it
            ticker_id = existing_ticker_id_result[0]

            # finally posting the articleticker row
            csr.execute(post_articleticker_query, (article_id, ticker_id, score))
            # update the running average
            csr.execute(update_ticker_score_query, (ticker_id,))

            # finding the sector id of the symbol
            csr.execute(get_sector_id_of_ticker_query, (ticker_id,))
            sector_id_result = csr.fetchone()

            # sector id running average calculation
            if sector_id_result is not None:
                csr.execute(update_sector_score_query, (sector_id_result,))

    except OracleProgrammingError as e:
        # printing some data
        print("Data:",data)
        print("Calculated score:", score)
        print(e)
        traceback.print_exc()

        # the reraise
        raise
    
    # committing insertions + updates
    cnx.commit()

# grabbing the api keys
api_key, api_secret_key = find_api_keys()

# initializing some variables
ml_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
ml_model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
ml_model.load_state_dict(torch.load('/var/lib/sentiments/ml_model.pth', map_location=torch.device('cpu')))

# subbing to the websocket api
data_stream = NewsDataStream(api_key=api_key, secret_key=api_secret_key)
data_stream.subscribe_news(socket_handler, "*")

# run
data_stream.run()