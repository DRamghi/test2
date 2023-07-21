import streamlit as st

import pandas as pd
import numpy as np

import base64

import io

from datetime import datetime, timedelta
import plotly.express as px

from konlpy.tag import Mecab

mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')

import re

from collections import Counter

##########################################
#페이지 기본설정
st.set_page_config(
    page_title="지면기사 분석 시스템",
    layout="wide",
)

col1, col2 = st.columns([1, 3])

with col1:
    st.header("지면기사 분석 시스템")
    st.subheader("원하는 키워드를 입력하세요")
    search_word = st.text_input("키워드", "예 : 대한민국")
    start_date = st.text_input("시작일자", "예 : 2022-11-03")
    end_date = st.text_input("종료일자", "예 : 2022-12-03")


with col2:
    st.header("분석결과")
    st.write(search_word)
    st.write(start_date)
    st.write(end_date)

###########################################

data = pd.read_csv("C:\\github\\project3\\full_result_diet.csv")
data['Date'] = data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])
data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

########## 특정 키워드 빈도수 ##################
# 대상기간 내 기사 본문 추출
date_data = data[data['Date'].between(start_date, end_date)]

# 특정 키워드 기사 index 추출(제목에 포함 or 본문에 3번 이상 포함)
target_index_list = []
for i in range(0, len(date_data)):
    title_i = date_data.iloc[i, 2]
    if title_i.count(search_word) > 0:
        target_index_list.append(i)

result_list = date_data.iloc[target_index_list]

full_date_list = pd.date_range(start=start_date, end=end_date)
date_list = set(result_list['Date'])
date_list = list(date_list)
date_list.sort(reverse=False)

target_date_list = []
count = []
for i in full_date_list:
    if i in date_list:
        a = result_list[result_list['Date'] == i]  # 특정 일자의 기사 불러오기
        b = a['Title'].tolist()
        b = ' '.join(b)
        count.append(b.count(search_word))
        target_date_list.append(i)
    else:
        count.append(0)
        target_date_list.append(i)

d = pd.DataFrame([target_date_list, count])
if len(target_date_list) < 10:
    width = 5
elif len(target_date_list) < 20:
    width = 10
else:
    width = 15

d = d.transpose()  # 행 열 전환
d.rename(columns={0: "date"}, inplace=True)
d.rename(columns={1: "count"}, inplace=True)

import plotly.express as px

fig = px.line(d, x="date", y="count")








#######################################################

