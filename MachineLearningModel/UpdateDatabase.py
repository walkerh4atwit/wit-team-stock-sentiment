import pandas as pd
import oracledb

data = pd.read_csv("MachineLearningModel/finhub_data_sentiment.csv")

connection=oracledb.connect(
     config_dir=r"D:\WIT\Senior Project\Wallet_database1",
     user="admin",
     password="Database1Pass",
     dsn="database1_low",
     wallet_location=r"D:\WIT\Senior Project\Wallet_database1",
     wallet_password="Password1")

cursor = connection.cursor()

check_query = """
SELECT COUNT(*) FROM Tickers WHERE ticker = :1
"""
update_query = """
UPDATE Tickers SET sentiment_score = :1 WHERE ticker = :2
"""
insert_query = """
INSERT INTO Tickers (ticker, sentiment_score)
VALUES (:1, :2)
"""

for index, row in data.iterrows():
     ticker = row['ticker']
     sentiment_score = row['sentiment']
            
     cursor.execute(check_query, (ticker,))
     count = cursor.fetchone()[0]
            
     if count > 0:
          cursor.execute(update_query, (sentiment_score, ticker))
          print(f"Updated sentiment score for {ticker}")
     else:
          cursor.execute(insert_query, (ticker, sentiment_score))
          print(f"Inserted new ticker {ticker}")
        
connection.commit()
print("Database update complete")