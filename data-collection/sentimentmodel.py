import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Note that the loaded model will default to cuda device, including for inference.

device = 'cuda' if torch.cuda.is_available() else 'cpu'
label_to_num = {"positive": 2, "neutral": 1, "negative": 0}

BATCH_SIZE = 16
MAX_LEN = 512
EPOCHS = 1


class NewsDataset(Dataset):
    def __init__(self, content, labels, tokenizer, max_length, label_to_num):
        self.content = content
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.label_to_num = label_to_num

    def __len__(self):
        return len(self.content)

    def __getitem__(self, idx):
        content = self.content[idx]
        label = self.labels[idx]
        label_id = self.label_to_num[label]
        encoding = self.tokenizer(
            content,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt')
        return encoding['input_ids'].squeeze(), encoding['attention_mask'].squeeze(), torch.tensor(label_id)


df = pd.read_csv("train_data0.csv")
content = df['headline'].to_list()
labels = df['score'].to_list()

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

train_content, test_content, train_labels, test_labels = train_test_split(content, labels, test_size=0.2)

train_dataset = NewsDataset(train_content, train_labels, tokenizer, MAX_LEN, label_to_num)
test_dataset = NewsDataset(test_content, test_labels, tokenizer, MAX_LEN, label_to_num)

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
#model.load_state_dict(torch.load("saved-models/bert_model_512.pth"))

model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
criterion = torch.nn.CrossEntropyLoss()

stepi = []
lossi = []
acci = []
correct = 0
total = 0
i = 0
for epoch in range(EPOCHS):
    model.train()
    for batch in train_dataloader:
        input_ids, attention_mask, labels = batch
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        print(f"{i} ___ loss: {loss}")
        i += 1

        ### eval metrics
        #preds = torch.argmax(outputs.logits, dim=1)
        #total += labels.size(0)
        #correct += (preds == labels).sum().item()

        stepi.append(i)
        lossi.append(loss.item())
        #acci.append(correct / total)

    print(f"epoch: {epoch}")

torch.save(model.state_dict(), "saved-models/bert_model_512.pth")


model.eval()
with torch.no_grad():
    for batch in test_dataloader:
        input_ids, attention_mask, labels = batch
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        preds = torch.argmax(outputs.logits, dim=1)
        total += labels.size(0)
        correct += (preds == labels).sum().item()

print(f"Accuracy: {correct / total}")

#plt.plot(stepi, lossi, acci)
#plt.show()