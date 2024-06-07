from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import pandas as pd
import oracledb

#Process Data
data = pd.read_csv("MachineLearningModel/alpaca_news_data.csv")
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

data.to_csv('MachineLearningModel/alpaca_sentimts.csv')


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
SELECT COUNT(*) FROM Tickers WHERE title = :1
"""
get_ticker_id_query = """
SELECT id FROM Tickers WHERE ticker = :1
"""
get_article_id_query = """
SELECT id FROM Tickers WHERE title = :1
"""
insert_ticker_query = """
INSERT INTO Tickers (ticker)
VALUES (:1, :2)
"""
insert_article_query = """
INSERT INTO Articles (title, url, summary, data_published)
VALUES (:1, :2, :3, :4)
"""
insert_articleticker_query = """
INSERT INTO ArticleTickers (article_id, ticker_id, sentiment_score)
VALUES (:1, :2, :3, :4)
"""

#Create Tickers if not in DB else just update sentiment
for index, row in data.iterrows():
    newArticle = False
    article = row['headline']
    sentiment_score = row['sentiment']
    cursor.execute(check_article_query, (article,))
    countArticle = cursor.fetchone()[0]

    if countArticle == 0:
        cursor.execute(insert_article_query, (article, row['url'], row['summary'], row['created_at']))
        print(f"Inserted new article {article}")
        newArticle = True

    for ticker in row['symbols']:
            
        cursor.execute(check_ticker_query, (ticker,))
        countTicker = cursor.fetchone()[0]
            
        if countTicker == 0:
            cursor.execute(insert_ticker_query, (ticker))
            print(f"Inserted new ticker {ticker}")

        if newArticle:
            cursor.execute(get_ticker_id_query, (ticker,))
            ticker_id = cursor.fetchone()[0]
            cursor.execute(get_article_id_query, (article,))
            article_id = cursor.fetchone()[0]
            cursor.execute(insert_articleticker_query, (article_id,ticker_id,sentiment_score))


        
        
connection.commit()
print("Database update complete")