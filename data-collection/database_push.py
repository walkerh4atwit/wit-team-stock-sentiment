from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import oracledb
from datetime import datetime


def connect_to_db():
    connection = oracledb.connect(
        config_dir="Wallet_database1",
        user="admin",
        password="Database1Pass",
        dsn="database1_low",
        wallet_location="Wallet_database1",
        wallet_password="Password1"
    )
    return connection


def push_article(headline, url, summary, date_published):
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()

    check_article_query = """
    SELECT COUNT(*) FROM Articles WHERE url = :1
    """
    insert_article_query = """
    INSERT INTO Articles (title, url, summary, date_published)
    VALUES (:1, :2, :3, TO_TIMESTAMP(:4, 'YYYY-MM-DD HH24:MI:SS'))
    """
    cursor.execute(check_article_query, (url,))
    countArticle = cursor.fetchone()[0]

    if countArticle == 0:
        oracle_datetime = date_published.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(insert_article_query, (headline, url, summary, oracle_datetime))
        print(f"Inserted new article {headline}")
    connection.commit()
    print("Database update complete")


def push_article_ticker(url, symbols, score):
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()

    # SQL queries for db communication
    check_ticker_query = """
    SELECT COUNT(*) FROM Tickers WHERE ticker = :1
    """
    get_ticker_id_query = """
    SELECT id FROM Tickers WHERE ticker = :1
    """
    get_article_id_query = """
    SELECT id FROM Articles WHERE url = :1
    """
    insert_ticker_query = """
    INSERT INTO Tickers (ticker)
    VALUES (:1)
    """
    insert_articleticker_query = """
    INSERT INTO ArticleTickers (article_id, ticker_id, sentiment_score)
    VALUES (:1, :2, :3)
    """
    for ticker in str(symbols)[2:-2].split("', '"):
        if ticker == "":
            continue

        cursor.execute(check_ticker_query, (ticker,))
        countTicker = cursor.fetchone()[0]

        if countTicker == 0:
            cursor.execute(insert_ticker_query, (ticker,))
            print(f"Inserted new ticker {ticker}")

        cursor.execute(get_ticker_id_query, (ticker,))
        ticker_id = cursor.fetchone()[0]
        cursor.execute(get_article_id_query, (url,))
        article_id = cursor.fetchone()[0]
        cursor.execute(insert_articleticker_query, (article_id, ticker_id, score))

    connection.commit()
    print("Database update complete")


def delete_old_articles():
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()

    delete_query = """
    DELETE FROM Articles
    WHERE DATE_PUBLISHED < SYSDATE - 7

    DELETE FROM Tickers
    WHERE id NOT IN (
    SELECT DISTINCT ticker_id
    FROM ArticleTickers
    );
    """

    cursor.execute(delete_query)
    connection.commit()
    print("Deleted articles older than 7 days")

    cursor.close()
    connection.close()


