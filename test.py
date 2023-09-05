import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import re
import numpy as np
import math
from konlpy.tag import Mecab
from collections import Counter
import random

import plotly.graph_objects as go
import plotly.express as px

mecab = Mecab()

line = "후쿠시마 원전 오염수는 안전한가?"
nouns = mecab.nouns(line)
print(nouns)


# file_path = "/home/ubuntu/test2/full_result.csv"
# data = pd.read_csv(file_path)

#################################################################.


#data = pd.read_csv("/home/ubuntu/test2/today_department_table.csv")
# data = pd.read_csv("/home/ubuntu/test2/full_result.csv")
# del data['Unnamed: 0']
# data['Date'] = data['Date'].astype('str')
# data['Date'] = pd.to_datetime(data['Date'])

# print(data.iloc[0, 0])
# print(data.iloc[0, 1])
# print(data.iloc[0, 2])
# print(data.iloc[0, 3])

#del today_data['Unnamed: 0']

#data['Date'] = data['Date'].astype('str')
#data['Date'] = pd.to_datetime(data['Date'])

# import time
# from datetime import datetime, timedelta
# from pytz import timezone

#days = ['월', '화', '수', '목', '금', '토', '일']


#now = datetime.now(timezone('Asia/Seoul'))
#a = days[datetime.date(now).weekday()]


#data = data.replace({'Date' : '20230818'}, '2023-08-18') 
#data = data.replace({'Date' : '20230817'}, '2023-08-17') 


#data = data[data.Press != '문화일보']


#a = data[data['Date']=='2023-08-05']
#a = a['Sentiment']

#b = b[100]
#print(b)


#a['Date'] = pd.to_datetime(a['Date']) 
#b = a.loc[37937,'Date']
#b = b[100]
#print(b)
#print(type(b))
#a = list(set(data['Date']))
#a.sort()
#print(a)
# a =data[data['Date']=='20230816']
# a = a.drop_duplicates(['Body'], keep='first')

# b = data[data['Date']=='2023-08-16']
# b = b.drop_duplicates(['Body'], keep='first')
#print(len(a), len(b))
#print(len(a[a['Press']=='조선일보']))

#print(len(b[b['Press']=='조선일보']))
#a.to_csv("/home/ubuntu/test2/20230816.csv")
#b.to_csv("/home/ubuntu/test2/2023-08-16.csv")
#data[data['Date']=='20230817']['Date'] = "2023-08-17"
#data.to_csv("/home/ubuntu/test2/full_result.csv")
#data[data['Date']=='20230818']['Date'] = "2023-08-18"
#a = data['Date']
#a = a[39000]
#print(a, type(a))
#pd.to_datetime(data['Date'])
#b = b[39000]
#a = len(a)
#print(b, type(b))

#date = now.date()


#count = 0
#for j in range(0, len(a)):
#    title_j = a.iloc[j, 2]
#    body_j = a.iloc[j, 4]
#    if title_j.count(search_word) > 0 or body_j.count(search_word) > 0:
#        count = count + title_j.count(search_word) + body_j.count(search_word)
#        index_list.append(a.index[j])
#        if date_list.count(i) == 0:
#            date_list.append(i)
#count_list.append(count)

#today_data['Weekday']=""
#for i in range(0, len(today_data)):
#    today_data['Weekday'][i] = days[datetime.date(today_data['Date'][i]).weekday()]
#print(today_data['Weekday'][10000], today_data['Date'][10000])
