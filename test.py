import pandas as pd
data = pd.read_csv("/home/ubuntu/test2/full_result.csv")

print(set(data['Date']))