import pandas as pd
import oracledb

def getTickers():
    connection=oracledb.connect(
        config_dir="Wallet_database1",
        user="backend",
        password="Password123@",
        dsn="database1_low",
        wallet_location="Wallet_database1",
        wallet_password="Password1"
    )

    cursor = connection.cursor()
    result = {}

    # ID, NAME, COMPANY, COUNT
    query_file = open('queries/ArticlesTickersCount.sql', 'r')
    query_string = query_file.read()
    query_file.close()

    cursor.execute(query_string)
    result['stock'] = cursor.fetchall()

    # ID, SECTOR, COUNT
    query_file = open('queries/ArticlesSectorsCount.sql', 'r')
    query_string = query_file.read()
    query_file.close()
    
    cursor.execute(query_string)
    result['sector'] = cursor.fetchall()

    return result