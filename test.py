import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import re
import numpy as np
import math
from konlpy.tag import Mecab
from collections import Counter
import random
import pickle

import plotly.graph_objects as go
import plotly.express as px

from kiwipiepy import Kiwi

from jamo import h2j, j2hcj

#mecab = Mecab()

# stop_words = "이번 담당 여러분 관련 이날 이후 오후 오전 경우 기간 때문 당시 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간 지난달"

#noun = "이날"

#if len(noun) > 1 and noun not in stop_words and noun != search_word:
#    print(noun)

#dict = {"이날" : 1}
#print(dict['이날'])

# file_path = "/home/ubuntu/test2/full_result.csv"
# data = pd.read_csv(file_path)

#################################################################.


#data = pd.read_csv("/home/ubuntu/test2/today_department_table.csv")
#data = pd.read_csv("/home/ubuntu/test2/full_result.csv")
data = pd.read_csv("/home/ubuntu/test2/231012.csv")

#a = data[data['Date']=="2023-10-12"]
#b = a['Press']
# c = a['Title']
print(data)



# data4 = data[data['Date']=="2023-08-19"]
# print(len(data4))

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
#print(now.weekday())
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

###################################################################
#kiwi 신규단어 자체사전에 추가
# kiwi = Kiwi()


# file_path = "/home/ubuntu/test2/full_result.csv" 
# data = pd.read_csv(file_path)

# data['Date'] = data['Date'].astype('str')
# data['Date'] = pd.to_datetime(data['Date'])
# data.reset_index(drop=True, inplace=True)
# del data['Unnamed: 0']

# start_date = "2023-07-06"
# end_date = "2023-07-07"

# start_date = datetime.strptime(start_date, '%Y-%m-%d')
# end_date = datetime.strptime(end_date, '%Y-%m-%d')

# date_data = data[data['Date'].between(start_date, end_date)] 

# text = date_data['Body']
# text.to_list()

#date_body = "이재명 대표에 대한 체포동의안이 가결되었다"
#tagger = Mecab()
#date_words = tagger.nouns(date_body)
#print(date_words)
# new_words = ["체포동의안"]


# new_noun_words = []
# for i in new_words:
#   if str(type(re.match("^[a-zA-Zㄱ-힣-]*$", i[0])))!="<class 'NoneType'>":
#    new_noun_words.append(i[0])
# new_noun_words

# print(new_noun_words)

# for i in new_noun_words:
#    kiwi.add_user_word(i, 'NNP', 0)
    
################################################################################
# import stylecloud

# text = {'채용': 84.0, '베트남': 81.0, '인천': 69.0, '현대': 61.0, '모로코': 61.0, '위원장': 56.0, '김정은': 54.0, '법원': 54.0, '방송': 52.0, '포스코': 50.0, '바이든': 48.0, '해임': 47.0, '푸틴': 47.0, '보험': 46.0, '지분': 42.0, '선관위': 42.0, '정상회담': 40.0, '단식': 40.0, '유치': 39.0, '경쟁': 38.0, '관계': 37.0, '고려대': 36.0, '분양': 35.0, '무기': 34.0, '보호': 34.0, '지구': 34.0, '수생': 32.0, '이사장': 32.0, '탄핵': 32.0, '울산 시장': 32.0, '열차': 32.0, '하반기': 31.0, '포럼': 30.0, '방 문진': 30.0, '이해수': 30.0, '선거 개입': 29.0, '예술': 29.0, '바이오': 29.0, '전력': 29.0, '수능': 28.0, '지하철': 28.0, '송철호': 27.0, '이용': 27.0, '비리': 27.0, '김만배': 27.0, '지진': 26.0, '비중': 26.0, '전지': 26.0, '국무 위원장': 26.0, '빅 테크': 26.0}

# print(len(text))
# stylecloud.gen_stylecloud(text = text,
#                           #palette="cartocolors.diverging.TealRose_7", #"colorbrewer.diverging.Spectral_11",
#                           background_color='white',
#                           #gradient="horizontal",
#                           output_name="test.png",
#                           font_path='NanumGothic.ttf')

#########################
# save kiwi_new_word

# kiwi_word = ['게티이미지뱅크', '도우주연구기구', '클로바X', '하이퍼클로바X', 'C현대산업개발', '챗GPT', 'SK바이오사이언스', '포스코퓨처엠', '대구경북통합신공항', '포스코인터내셔널', '두산에너빌리티', 'LG에너지솔루션', '바이오사이언스', 'G모빌리티', '문화체육관광부', '농림축산식품부', '플레이션', '감축법', 'AFP연합뉴스', 'HD현대중공업', '바이오로직스', '저축은행', '렉트릭', '노란봉투법', '스카이셀플루', '대규모유통업법', '과학기술정보통신부', 'HD한국조선해양', '특례보금자리론', '방송통신위원회', '중소벤처기업부', '공산전체주의', '학생부종합전형', '스노우피크', 'DL이앤씨', '산업통상자원부', '컨트롤타워', '학생인권조례', '오모빌리티', '소상공인', '민원대응팀', '포스코이앤씨', '잭슨홀', '노동조합총연맹', '로이터연합뉴스', 'K칩스법', '자립준비청년', '한화에어로스페이스', '팝업스토어', '투자증권', '지방자치단체', 'AP연합뉴스', '관동대지진', '사회관계망서비스', '지방교육재정교부금', '한화오션', '다핵종제거설비', '국토교통부', '비구이위안', '취약계층', '공정거래위원회', '특별위원회', '중소벤처기업', '재생에너지', '게티이미지', '레이션', '스마트싱스', '저소득층', '롯데웰푸드', '기후변화', '국가산업단지', '금융지주', '인플레이션감축법', '정보시스템', '디즈니플러스', '공영방송', '물가상승률', '언어모델', '시교육청', '도교육청', '반국가세력', '질병관리청', '라마스와미', '세계청년대회', '니케이션', '새만금국제공항', '어린이보호구역', '튀르키예', '탄도미사일', '정경유착', '스텔란티스', '아이돌보미', '서울동행버스', '군사동맹', '세액공제', '코플랜트', '해양수산부', '국민권익위원회', '바그너그룹', '고용노동부', '순항미사일', '이상동기범죄', '빌리티', '자치단체', '도교육감', '사법입원제', '행정안전부', '가짜뉴스', 'HD현대', '로보틱스', '첨단전략산업', '카카오뱅크', '시립미술관', '흉악범죄', '학생부교과전형', '교육지원청', '하이퍼클로바', '자율주행', '지원센터', '김포골드라인', '억달러', '저신용자', '협중앙회', '대책위원회', '공정거래']

# with open('kiwi_word.pkl', 'wb') as f:
#     pickle.dump(kiwi_word, f)

#with open('kiwi_word.pkl', 'rb') as f:
#    new_word = pickle.load(f)

#print(new_word)  


# subword_list = [['국방부', '장관'], ['국방', '장관']]

# del_list = []
# for i in subword_list:
#   for j in subword_list:
#     if i == j:
#       pass
#     else:
#       same = [x for x, y in zip(i,j) if x == y]  #두 리스트 비교, 같은 값 개수 확인
#       if len(same)/(len(i)=len(j)) > 0.7 :
#         if len(i) > len(j):
#             del_list.append(' '.join(j))

#a = "징역 년"
#print(a[-3:])




#######################

#text = "20명"
#a=re.match("[0-9]*명", text)
#print(a)

# new_words = ["해명", "100일", "1만원", "만9000", "000억"]
# new_noun_words = []
# for i in new_words:
#   if str(type(re.match("^[(만|억)*[0-9]+[ㄱ-힣]*]", i)))=="<class 'NoneType'>":
#    new_noun_words.append(i)
# print(new_noun_words)



# kiwi = Kiwi()


# file_path = "/home/ubuntu/test2/full_result.csv" 
# data = pd.read_csv(file_path)

# data['Date'] = data['Date'].astype('str')
# data['Date'] = pd.to_datetime(data['Date'])
# data.reset_index(drop=True, inplace=True)
# del data['Unnamed: 0']

# #now = datetime.now(timezone('Asia/Seoul'))
# #today = str(now.date())


# start_date = datetime.strptime("2023-10-01", '%Y-%m-%d')
# end_date = datetime.strptime("2023-10-07", '%Y-%m-%d')

# date_data = data[data['Date'].between(start_date, end_date)] 

# text = date_data['Body']
# text.to_list()

# new_words = kiwi.extract_add_words(text, 10, 15, 0.2, -3., True)

# new_noun_words = []
# for i in new_words:
#   if str(type(re.match("^[a-zA-Z0-9ㄱ-힣-]*$", i[0])))!="<class 'NoneType'>":
#     if str(type(re.match("[0-9]*[ㄱ-힣]*[0-9]+[ㄱ-힣]*(명|원|일|달러|개|백|천|억|만)", i[0])))=="<class 'NoneType'>":
#         if str(type(re.match("(만|억)*[0-9]+", i[0])))=="<class 'NoneType'>":
#             new_noun_words.append(i[0])
# new_noun_words

# print(new_noun_words)