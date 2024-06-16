from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

#mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis


def model_function(df_slice):

    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    tokens = tokenizer.encode(df_slice['headline-summary'], return_tensors='pt')
    result = model(tokens)
    score = int(torch.argmax(result.logits))+1
    print(score, " ----- ", df_slice['headline-summary'])
