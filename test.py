import pandas as pd
data = pd.read_csv("/home/ubuntu/test2/full_result.csv")
del data['Unnamed: 0']

a = data['Date'][0]
print(a,type(a))