import pandas as pd

a = pd.read_csv("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-nnp.csv")
a.iloc[:,3] = 1

a.rename(columns={a.columns[3]:1}, inplace=True)
a.rename(columns={a.columns[7]:a.columns[0]}, inplace=True)
a.rename(columns={a.columns[8]:"*"}, inplace=True)
a.rename(columns={a.columns[9]:"*"}, inplace=True)
a.rename(columns={a.columns[10]:"*"}, inplace=True)
a.rename(columns={a.columns[11]:"*"}, inplace=True)
a.rename(columns={a.columns[12]:"*"}, inplace=True)

a.to_csv('/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user_nnp.txt', index=False)

with open('/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user_nnp.txt', 'r', encoding='utf-8') as f:
  file_data = f.readlines()

with open("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-nnp.csv", 'w', encoding='utf-8') as f:
  for line in file_data:
    f.write(line)


with open('/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-nnp.csv', 'r', encoding='utf-8') as f:
  file_data = f.readlines()

print(file_data)