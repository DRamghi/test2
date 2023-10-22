
import re
from kiwipiepy import Kiwi
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import pickle


with open("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
    file_data = f.readlines()
new = []

for i in file_data:
    if i in new:
        print(i)
        pass
    else:
        new.append(i)
print(len(file_data))
print(len(new))