from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import pandas as pd


data = pd.read_csv("MachineLearningModel/finnhub_data.csv")
data['text'] = data['headline'] + " " + data['summary']
text = data[['text']]
text.dropna(inplace=True)
print(text)

tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = TFBertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


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

max_length = 128

input_ids, attention_masks = encode_texts(text['text'].values, tokenizer, max_length)

predictions = model.predict({'input_ids': input_ids, 'attention_mask': attention_masks})

predicted_classes = tf.math.argmax(predictions.logits, axis=-1).numpy()

text['sentiment'] = predicted_classes

sentiment_mapping = {
    0: 'Very Negative',
    1: 'Negative',
    2: 'Neutral',
    3: 'Positive',
    4: 'Very Positive'
}

text['ticker'] = 'AAPL'

aggregate = text[['sentiment','ticker']].groupby(['ticker']).mean()

aggregate['sentiment'] = int(round(aggregate['sentiment'],0))

sentiment_mapping = {
    0: 'Very Negative',
    1: 'Negative',
    2: 'Neutral',
    3: 'Positive',
    4: 'Very Positive'
}

aggregate['sentiment_interpretation'] = text['sentiment'].map(sentiment_mapping)

print(aggregate)

aggregate.to_csv('MachineLearningModel/finhub_data_sentiment.csv')