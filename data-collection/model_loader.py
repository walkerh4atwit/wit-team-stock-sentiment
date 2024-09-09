from transformers import BertForSequenceClassification, BertTokenizer
import torch
import database_push


def model_function(text, symbols, url):

    num_to_label = {2: 'positive', 1: 'neutral', 0: 'negative'}

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
    model.load_state_dict(torch.load('14-48bm128.pth', map_location=torch.device('cpu')))

    tokens = tokenizer.encode(text, return_tensors='pt')
    result = model(tokens)
    score = torch.argmax(result.logits).item()
    print(num_to_label[score], " ----- ", text)
    database_push.push_article_ticker(url,symbols,score)
