from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import oracledb
from datetime import datetime

#mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis


def model_function(df_slice):

    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    tokens = tokenizer.encode(df_slice['headline-summary'], return_tensors='pt')
    result = model(tokens)
    score = int(torch.argmax(result.logits))+1
    print(score, " ----- ", df_slice['headline-summary'])
    #connect to db
    connection=oracledb.connect(
        config_dir=r"D:\WIT\Senior Project\Wallet_database1",
        user="admin",
        password="Database1Pass",
        dsn="database1_low",
        wallet_location=r"D:\WIT\Senior Project\Wallet_database1",
        wallet_password="Password1")

    cursor = connection.cursor()

    #SQL queries for db communication 
    check_ticker_query = """
    SELECT COUNT(*) FROM Tickers WHERE ticker = :1
    """
    check_article_query = """
    SELECT COUNT(*) FROM Articles WHERE title = :1
    """
    get_ticker_id_query = """
    SELECT id FROM Tickers WHERE ticker = :1
    """
    get_article_id_query = """
    SELECT id FROM Articles WHERE title = :1
    """
    insert_ticker_query = """
    INSERT INTO Tickers (ticker)
    VALUES (:1)
    """
    insert_article_query = """
    INSERT INTO Articles (title, url, summary, date_published)
    VALUES (:1, :2, :3, TO_TIMESTAMP(:4, 'YYYY-MM-DD HH24:MI:SS'))
    """
    insert_articleticker_query = """
    INSERT INTO ArticleTickers (article_id, ticker_id, sentiment_score)
    VALUES (:1, :2, :3)
    """
    newArticle = False
    article = df_slice['headline']
    sentiment_score = score
    cursor.execute(check_article_query, (article,))
    countArticle = cursor.fetchone()[0]

    if countArticle == 0:

        created_at = df_slice['created_at']
        print(created_at)
        oracle_datetime = created_at.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(insert_article_query, (article, df_slice['url'], df_slice['summary'], oracle_datetime))
        print(f"Inserted new article {article}")
        newArticle = True

    for ticker in str(df_slice['symbols'])[2:-2].split("', '"):
        if ticker == "":
            continue
                    
        cursor.execute(check_ticker_query, (ticker,))
        countTicker = cursor.fetchone()[0]
                    
        if countTicker == 0:
            cursor.execute(insert_ticker_query, (ticker,))
            print(f"Inserted new ticker {ticker}")

        if newArticle:
            cursor.execute(get_ticker_id_query, (ticker,))
            ticker_id = cursor.fetchone()[0]
            cursor.execute(get_article_id_query, (article,))
            article_id = cursor.fetchone()[0]
            cursor.execute(insert_articleticker_query, (article_id,ticker_id,sentiment_score))


            
            
    connection.commit()
    print("Database update complete")
    
    
