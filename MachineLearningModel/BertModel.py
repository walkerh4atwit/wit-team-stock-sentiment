from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import pandas as pd
import oracledb
from datetime import datetime

#Process Data
data = pd.read_csv("MachineLearningModel/alpaca_news_data_update.csv")
data['text'] = data['headline'] + " " + data['summary']
data.dropna(subset=['text'],inplace=True)


#Initialize Model
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = TFBertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

#Function to Encode Text
def encode_texts(texts, tokenizer, max_length):
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='tf',
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    return tf.squeeze(tf.convert_to_tensor(input_ids)), tf.squeeze(tf.convert_to_tensor(attention_masks))


max_length = 512

input_ids, attention_masks = encode_texts(data['text'].values, tokenizer, max_length)

#Make Predictions
predictions = model.predict({'input_ids': input_ids, 'attention_mask': attention_masks})

predicted_classes = tf.math.argmax(predictions.logits, axis=-1).numpy()

#Assign sentiments to tickers
data['sentiment'] = predicted_classes

data.to_csv('MachineLearningModel/alpaca_sentimts_update.csv')

exit()


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