import re
from kiwipiepy import Kiwi
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import pickle



from jamo import h2j, j2hcj
new_noun_words = ["국정감사"]

with open("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
  file_data = f.readlines()

for word in new_noun_words:
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
    pickle.dump("삼중수소", f)