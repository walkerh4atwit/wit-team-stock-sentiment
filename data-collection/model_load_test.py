from transformers import BertForSequenceClassification, BertTokenizer
import torch


def model_function(text):

    num_to_label = {2: 'positive', 1: 'neutral', 0: 'negative'}

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
    model.load_state_dict(torch.load('saved-models/bert_model_512.pth', map_location=torch.device('cpu')))

    tokens = tokenizer.encode(text, return_tensors='pt')
    result = model(tokens)
    score = torch.argmax(result.logits).item()
    print(num_to_label[score], " ----- ", text)
