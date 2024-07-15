import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizer
import torch


def filter_ticker():
    df = pd.read_csv("../csv/companies.csv")
    df = df.loc[:, df.columns.intersection(['ticker', 'short name', 'ceo'])]
    df.to_csv("ticker_to_name.csv")


def add_ticker_to_csv():
    train = pd.read_csv("train_data1.csv")
    tickers = pd.read_csv("../csv/ticker_to_name.csv")

    for i in range(len(train['headline'])):
        content = train.loc[i, 'headline']
        for j in range(len(tickers['short name'])):
            company_name = tickers.loc[j, 'short name']
            print(i * 4846 + j)
            if company_name in content:
                train.loc[i, 'ticker'] = tickers.loc[j, 'ticker']

    train.to_csv("train_data2.csv")


def del_no_ticker():
    data = pd.read_csv("mc_dataset.csv")
    for i in range(len(data['symbols'])):
        if data.loc[i, 'symbols'] == "[]":
            data.drop(i, inplace=True)

    data.drop(columns=['Unnamed: 0', 'author', 'updated_at', 'content', 'url', 'images', 'source'], inplace=True)
    data.to_csv("mc_dataset.csv", index=False)


def extrapolate_tickers():
    data = pd.read_csv("../csv/mc_dataset2.csv")
    for i in range(len(data['symbols'])):
        t = data.loc[i, 'symbols'].split()
        converted_list = []
        for item in t:
            converted_list.append(item.replace('[', '').replace(']', '').replace('\'', '').replace(',', ''))
        print(converted_list)


def extrapolate_ticker(dataloc_item):
    t = dataloc_item.split()
    converted_list = []
    for item in t:
        converted_list.append(item.replace('[', '').replace(']', '').replace('\'', '').replace(',', ''))
    return converted_list


def del_multi_tickers():
    data = pd.read_csv("../csv/mc_dataset2.csv")
    for i in range(len(data['symbols'])):
        t = data.loc[i, 'symbols']
        ticker_list = extrapolate_ticker(t)
        if len(ticker_list) > 1:
            data.drop(i, inplace=True)

    data.to_csv("mc_single_ticker_dataset.csv", index=False)


def label_types():
    data = pd.read_csv("../csv/rating_dataset.csv")
    nan, two, one, zero = 0, 0, 0, 0
    for i in range(len(data['symbols'])):
        t = data.loc[i, 'label']
        if t == 2.0:
            two += 1
        elif t == 1.0:
            one += 1
        elif t == 0.0:
            zero += 1
        else:
            nan += 1
    print(nan, two, one, zero)


def del_no_label():
    data = pd.read_csv("../csv/rating_dataset.csv")
    for i in range(len(data['symbols'])):
        t = data.loc[i, 'label']
        if t != 2.0 and t != 1.0 and t != 0.0:
            data.drop(i, inplace=True)

    data.to_csv("rating_dataset.csv", index=False)


def model_inference(text):
    num_to_label = {2: 'positive', 1: 'neutral', 0: 'negative'}

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
    model.load_state_dict(torch.load('../saved-models/4-3e6bm512.pth'))

    tokens = tokenizer.encode(text, return_tensors='pt')
    result = model(tokens)
    pred = torch.argmax(result.logits).item()

    return pred


def test_model():
    data = pd.read_csv("../csv/rating_dataset.csv")
    correct = 0
    for i in range(len(data['headline'])):
        text = data.loc[i, 'headline']
        truth = int(data.loc[i, 'label'])
        pred = model_inference(text)
        if truth == pred:
            correct += 1
    print(correct, correct/111)


def mod_td0():
    data = pd.read_csv("../csv/train_data0.csv")
    pos, neg, neu = 0, 0, 0
    for i in range(len(data['score'])):
        t = data.loc[i, 'score']
        if t == 'positive':
            if pos < 400:
                pos += 1
            else:
                data.drop(i, inplace=True)

        elif t == 'negative':
            if neg < 400:
                neg += 1
            else:
                data.drop(i, inplace=True)

        elif t == 'neutral':
            if neu < 400:
                neu += 1
            else:
                data.drop(i, inplace=True)

    print(pos, neg, neu)

    data.to_csv("train_data1.csv", index=False)


mod_td0()