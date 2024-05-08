import finnhub
import pandas as pd

finnhub_client = finnhub.Client(api_key="cfj73ghr01que34nr220cfj73ghr01que34nr22g")

data = finnhub_client.general_news('general', min_id=0)

print(type(data))
print(len(data))
print(data[0])

df = pd.DataFrame(data)
df.to_csv('test.csv')
