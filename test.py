import pandas as pd
data = pd.read_csv("/home/ubuntu/test2/full_result.csv")

a = data[data['Date']==20230803]
b = data[data['Date']==20230804]
c = data[data['Date']==20230807]
print(len(a), len(b), len(c))

