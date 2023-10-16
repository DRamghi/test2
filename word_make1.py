import re
from kiwipiepy import Kiwi
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import pickle

kiwi = Kiwi()


file_path = "/home/ubuntu/test2/full_result.csv" 
data = pd.read_csv(file_path)

data['Date'] = data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])
data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

now = datetime.now(timezone('Asia/Seoul'))
today = str(now.date())

start_date = datetime.strptime(today, '%Y-%m-%d')
end_date = datetime.strptime(today, '%Y-%m-%d')

date_data = data[data['Date'].between(start_date, end_date)] 

text = date_data['Body']
text.to_list()

new_words = kiwi.extract_add_words(text, 10, 15, 0.2, -3., True)

new_noun_words = []
for i in new_words:
  if str(type(re.match("^[a-zA-Z0-9ㄱ-힣-]*$", i[0])))!="<class 'NoneType'>":
    if str(type(re.match("[0-9]*[ㄱ-힣]*[0-9]+[ㄱ-힣]*(명|원|일|달러|개|백|천|억|만)", i[0])))=="<class 'NoneType'>":
        if str(type(re.match("(만|억)*[0-9]+", i[0])))=="<class 'NoneType'>":
            new_noun_words.append(i[0])
new_noun_words

print(new_noun_words)


from jamo import h2j, j2hcj

previous_word = pd.read_csv("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv")
previous_word_set = set(previous_word.iloc[:,0].to_list())



with open('/home/ubuntu/test2/kiwi_word.pkl', 'rb') as f: # 불러오기
    new_word_kiwi = pickle.load(f)
new_word_kiwi_set = set(new_word_kiwi)

#print(new_word_kiwi)


with open("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
  file_data = f.readlines()

for word in new_noun_words:
  if word not in new_word_kiwi_set :
    new_word_kiwi.append(word)
    if word not in previous_word_set :
      sample_text_list = list(word)
      last_word = sample_text_list[-1]
      last_word_jamo_list = list(j2hcj(h2j(last_word)))
      last_jamo = last_word_jamo_list[-1]

      jongsung_TF = "T"

      if last_jamo in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅘ', 'ㅚ', 'ㅙ', 'ㅝ', 'ㅞ', 'ㅢ', 'ㅐ,ㅔ', 'ㅟ', 'ㅖ', 'ㅒ']:
          jongsung_TF = "F"

      line = '{},,,,NNP,*,{},{},*,*,*,*,*\n'.format(word, jongsung_TF, word)

      file_data.append(line)

#file_data = list(set(file_data))

with open("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'w', encoding='utf-8') as f:
  for line in file_data:
    f.write(line)



with open('/home/ubuntu/test2/kiwi_word.pkl', 'wb') as f: # 저장하기
    pickle.dump(new_word_kiwi, f)