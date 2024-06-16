import pandas as pd
import oracledb
from datetime import datetime

data = pd.read_csv("MachineLearningModel/alpaca_news_data_update.csv")


#connect to db
connection=oracledb.connect(
     config_dir=r"C:/Users/dyere1/Desktop/WIT Courses\Senior Project\Wallet_database1",
     user="admin",
     password="Database1Pass",
     dsn="database1_low",
     wallet_location=r"C:/Users/dyere1/Desktop/WIT Courses\Senior Project\Wallet_database1",
     wallet_password="Password1")

cursor = connection.cursor()

#SQL queries for db communication 
check_article_query = """
SELECT COUNT(*) FROM Articles WHERE title = :1
"""
get_article_id_query = """
SELECT id FROM Articles WHERE title = :1
"""

insert_article_query = """
INSERT INTO Articles (title, url, summary, date_published)
VALUES (:1, :2, :3, TO_TIMESTAMP(:4, 'YYYY-MM-DD HH24:MI:SS'))
"""
insert_queue_query = """
INSERT INTO Queue (article_id, date_added)
VALUES (:1, TO_TIMESTAMP(:2, 'YYYY-MM-DD HH24:MI:SS'))
"""


for index, row in data.iterrows():
    newArticle = False
    article = row['headline']
    cursor.execute(check_article_query, (article,))
    countArticle = cursor.fetchone()[0]

    if countArticle == 0:
        
        created_at = row['created_at']
        parsed_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        oracle_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")

        print(article, row['url'], row['summary'], oracle_datetime)

        cursor.execute(insert_article_query, (article, row['url'], str(row['summary']), oracle_datetime))
        print(f"Inserted new article {article}")
        newArticle = True
        cursor.execute(get_article_id_query, (article,))
        article_id = cursor.fetchone()[0]
        cursor.execute(insert_queue_query, (article_id, oracle_datetime))




        
        
connection.commit()
print("Database update complete")