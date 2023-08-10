import pandas as pd
data = pd.read_csv("/home/ubuntu/test2/full_result.csv")
del data['Unnamed: 0']

a = set(data['Date'])
print(a)