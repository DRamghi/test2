import pandas as pd
from collections import Counter # 텍스트 및 빈도수 추출
import numpy as np #불러온 그림을 배열로 나타내어 쉽게 처리할 수 있도록 도와주는 패키지
import time
from tqdm import tqdm
from datetime import datetime, timedelta
from pytz import timezone

from konlpy.tag import Mecab
mecab = Mecab()

stop_words = "이번 담당 여러분 관련 이날 이후 오후 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간"
stop_words = set(stop_words.split(' '))

data = pd.read_csv("/home/ubuntu/test2/full_result.csv")

# Date의 dtype를 Datetime으로 변경
data['Date']= data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])

#인덱스 초기화, 불필요한 컬럼 제거
data.reset_index(drop = True, inplace=True)
del data['Unnamed: 0']

#now = datetime.now(timezone('Asia/Seoul'))
#today = str(now.date())
#previous_day = now - timedelta(days=30)
#previous_day = str(previous_day)[:-22]
today = "2023-08-05"
previous_day = "2023-08-03"


#최근 1달간 DB 추출
sub_data = data[data['Date'].between(previous_day, today)]

date_range = list(set(sub_data['Date']))
date_range.sort()

##날짜별 키워드 빈도수 데이터프레임

add_stop_words = '우리 외부 현지 국가 계기 구성 현지시간 당시 현장 오늘 그날 참여 참석 계획 시일 의견 수렴 검토 요청 이유 논의 과정 결정 의미 확정 사업 회의 사건 조성 주변 사람 상태 누군가 정도 이곳 일대 당시 동안 마련 근처 정도 느낌 소식 그곳 이곳 이상'
add_stop_words = add_stop_words.split(' ')
add_stop_words.extend(list(stop_words))

keywords = pd.Series()
tagger = Mecab()
for i in tqdm(date_range):
  word_list = []
  date_body = data[data['Date'] == i]  #특정날짜에 해당하는 데이터프레임 추출
  date_body = date_body['Body'].tolist() # 해당 기사본문을 리스트화
  date_body = ' '.join(date_body)
  date_words = tagger.nouns(date_body)
  print(date_words)
  for word in date_words:
    if len(word)>1 and word not in add_stop_words:
      word_list.append(word)
  noun_count = Counter(word_list)
  noun_count = pd.Series(noun_count)
  noun_count.name = i
  keywords = pd.concat([keywords,noun_count], axis=1)
keywords = keywords.drop(0, axis=1)

#빈도수가 급증한 키워드 추출
a = keywords[((keywords.iloc[:,-1]>20)) & ((keywords.iloc[:,-1]>keywords.mean(axis='columns')*4) & (keywords.iloc[:,-1]>keywords.iloc[:,-2]))]
b = a.sort_values(by=[keywords.columns[-1]],ascending=False)
print(b)

#각 키워드별 연관검색어 추출 -> 데이터프레임에 병합
# top_words = b[0:50]
# today_data=data[data['Date']==today]
# related_words_table = []
# title_table = []
# url_table = []
# for n in range(0,50):
#   print(n)
#   search_word = b.index[n]
#   text = []
#   title_link_list = []
#   for i in range(0, len(today_data)):
#     title_i = today_data.iloc[i,2]
#     body_i = today_data.iloc[i,4]
#     url_i = today_data.iloc[i,1]
#     title_link_i = f'''<a href="{url_i}">{title_i})</a>'''
#     if title_i.count(search_word)>0 or body_i.count(search_word) >2:
#       text.append(body_i)
#       title_link_list.append(title_link_i)
#   text = ' '.join(text)
#   related_words = tagger.nouns(text)
#   related_words = [item for item in related_words if len(item)>1 and item != search_word]
#   related_words_count = Counter(related_words)
#   related_words_count = dict(related_words_count.most_common(7)).keys()
#   related_words_table.append(related_words_count)
#   title_table.append(title_link_list)

# title_table = pd.Series(title_table)
# title_table.name = "title_list"
# title_table.index = top_words.index
# related_words_table = pd.Series(related_words_table)
# related_words_table.index = top_words.index
# related_words_table.name = "연관어"
# related_words_table
# full_table = pd.concat([top_words, related_words_table, title_table], axis=1)
# full_table.to_csv("/issue.csv")

