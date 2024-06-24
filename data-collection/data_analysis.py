import pandas as pd
from transformers import BertTokenizer, LongformerTokenizer


def concat(df):

    for i in range(len(df['headline'])):
        item = df.loc[i, 'summary']
        if type(item) != float:
            df.loc[i, 'headline'] += " | "
            df.loc[i, 'headline'] += df.loc[i, 'summary']

    return df


def hsc(df):
    # this function checks which news items have all or some of the following items: headline, summary, and content
    a, sonly, conly = 0, 0, 0
    for row in range(10000):
        if type(df.loc[row, 'summary']) is not float and type(df.loc[row, 'headline']) is not float:
            a += 1
        elif type(df.loc[row, 'summary']) is not float:
            sonly += 1
        elif type(df.loc[row, 'content']) is not float:
            conly += 1
    print("-----")
    print(a)
    print(sonly)
    print(conly)


def hsc_counts(df):
    # this function counts the number of headlines, summaries, and content for a given dataframe
    headline = df['headline'].dropna().tolist()
    content = df['content'].dropna().tolist()
    summary = df['summary'].dropna().tolist()
    print("-----")
    print(len(headline))
    print(len(content))
    print(len(summary))


df = pd.read_csv("2024-06-22data.csv")

content = df['content'].dropna().tolist()
tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')
#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

token_counts = []
for c in content:
    token_counts.append(len(tokenizer.tokenize(c)))

print(max(token_counts))

total = 0
for item in token_counts:
    total += item

print(total / 4361)




#print(max(token_counts))


# content_size = len(tokenizer.tokenize(content))
# available_tokens = 512 - len(tokenizer.tokenize(headline))
# top = available_tokens / 2
# bottom = available_tokens - top

# model_content = headline + content.split()[:top] + content.split()[bottom:]
# tokens = tokenizer.tokenize(content)

