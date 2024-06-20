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

    query_ticker = 'SELECT * FROM ADMIN.TICKERS ORDER BY TICKER'
    query_sector = 'SELECT * FROM ADMIN.SECTORS ORDER BY NAME'
    
    cursor.execute(query_ticker)
    result['stock'] = cursor.fetchall()

    cursor.execute(query_sector)
    result['sector'] = cursor.fetchall()


    return result