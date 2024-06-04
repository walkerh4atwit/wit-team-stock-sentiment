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

    query = 'SELECT TICKER, COMPANY_NAME FROM ADMIN.TICKERS'
    
    cursor.execute(query)

    result = cursor.fetchall()

    print(result)

    return result

getTickers()