import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np

import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt

import base64
import io
from wordcloud import WordCloud
from datetime import datetime, timedelta
import plotly.express as px

from konlpy.tag import Mecab
mecab = Mecab()

import re

from collections import Counter

import plotly.graph_objects as go

##########################################
#페이지 기본설정
st.set_page_config(
    page_title="지면기사 분석",
    layout="wide",
)
#######################################################

file_path = "full_result.csv"
@st.cache_data
def load_data():
  data = pd.read_csv(file_path)
  return data

#################################################################.

data = load_data()
data['Date'] = data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])
data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']


def same_word(sentence):
    st = sentence
    st = re.sub('기재부', '기획재정부', st)
    st = re.sub('과기부', '과학기술정보통신부', st)
    st = re.sub('과기정통부', '과학기술정보통신부', st)
    st = re.sub('행안부', '행정안전부', st)
    st = re.sub('문체부', '문화체육관광부', st)
    st = re.sub('농식품부', '농림축산식품부', st)
    st = re.sub('산업부', '산업통상자원부', st)
    st = re.sub('산자부', '산업통상자원부', st)
    st = re.sub('고용부', '고용노동부', st)
    st = re.sub('여가부', '여성가족부', st)
    st = re.sub('국토부', '국토교통부', st)
    st = re.sub('해수부', '해양수산부', st)
    st = re.sub('중기부', '중소벤처기업부', st)
    st = re.sub('중기벤처부', '중소벤처기업부', st)
    st = re.sub('인사처', '인사혁신처', st)
    st = re.sub('인혁처', '인사혁신처', st)
    st = re.sub('식약처', '식품의약품안전처', st)
    st = re.sub('공정위', '공정거래위원회', st)
    st = re.sub('개인정보위', '개인정보보호위원회', st)
    st = re.sub('개보위', '개인정보보호위원회', st)
    st = re.sub('원안위', '원자력안전위원회', st)
    st = re.sub('국조실', '국무조정실', st)
    st = re.sub('국무총리실', '국무조정실', st)
    st = re.sub('대통령실', '대통령비서실', st)
    return st


def date_keyword_search(search_word, start_date, end_date): #날짜는 2022-11-10 형식으로 입력
  #키워드 입력
  #대상기간 내 기사 본문 추출
  date_data = data[data['Date'].between(start_date, end_date)]

  #특정 키워드 기사 index 추출(제목에 포함 or 본문에 3번 이상 포함)
  title_link_list = []
  press_list = []
  for i in range(0, len(date_data)):
    press = date_data.iloc[i, 0]
    link = date_data.iloc[i, 1]
    title = date_data.iloc[i,2]
    title_re = same_word(title)
    body = date_data.iloc[i,4]
    body_re = same_word(body)
    if title_re.count(search_word)>0 or body_re.count(search_word) >2:
        title_link = f'''<a href="{link}">{title} ({press})</a>'''
        title_link_list.append(title_link)

  search_time = len(title_link_list)
  search_result = pd.DataFrame({'기사 제목': title_link_list})
  search_result.index = search_result.index + 1

  fig = go.Figure(
      data=[
          go.Table(
              columnwidth=[3, 1],
              header=dict(
                  values=[f"<b>{i}</b>" for i in search_result.columns.to_list()],
                  # fill_color='blue'
              ),
              cells=dict(
                  values=search_result.transpose(),
                  align="left"
              )
          )
      ]
  )
  fig.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

  return search_time, fig



now = datetime.now(timezone('Asia/Seoul'))
today = str(now.date())


president_number, president = date_keyword_search("대통령비서실", today, today)
prime_number, prime = date_keyword_search("총리", today, today)
opm_number, opm = date_keyword_search("국무조정실", today, today)
moef_number, moef = date_keyword_search("기획재정부", today, today)
moe_number, moe = date_keyword_search("교육부", today, today)
msit_number, msit = date_keyword_search("과학기술정보통신부", today, today)
mofa_number, mofa = date_keyword_search("외교부", today, today)
unikorea_number, unikorea = date_keyword_search("통일부", today, today)
moj_number, moj = date_keyword_search("법무부", today, today)
mnd_number, mnd = date_keyword_search("국방부", today, today)
mois_number, mois = date_keyword_search("행정안전부", today, today)
mcst_number, mcst = date_keyword_search("문화체육관광부", today, today)
mafra_number, mafra = date_keyword_search("농림축산식품부", today, today)
motie_number, motie = date_keyword_search("산업통상자원부", today, today)
mohw_number, mohw = date_keyword_search("보건복지부", today, today)
me_number, me = date_keyword_search("환경부", today, today)
moel_number, moel = date_keyword_search("고용노동부", today, today)
mogef_number, mogef = date_keyword_search("여성가족부", today, today)
molit_number, molit = date_keyword_search("국토교통부", today, today)
mof_number, mof = date_keyword_search("해양수산부", today, today)
mss_number, mss = date_keyword_search("중소벤처기업부", today, today)
mpva_number, mpva = date_keyword_search("국가보훈부", today, today)
ftc_number, ftc = date_keyword_search("공정거래위원회", today, today)
fsc_number, fsc = date_keyword_search("금융위원회", today, today)
acrc_number, acrc = date_keyword_search("국민권익위원회", today, today)
pipc_number, pipc = date_keyword_search("개인정보보호위원회", today, today)
nssc_number, nssc = date_keyword_search("원자력안전위원회", today, today)
kcc_number, kcc = date_keyword_search("방송통신위원회", today, today)
mpm_number, mpm = date_keyword_search("인사혁신처", today, today)
moleg_number, moleg = date_keyword_search("법제처", today, today)
mfds_number, mfds = date_keyword_search("식품의약품안전처", today, today)



name_list = ["대통령비서실", "국무총리", "국무조정실", "기획재정부", "교육부", "과학기술정보통신부", "외교부", "통일부", "법무부", "국방부",
             "행정안전부", "문화체육관광부", "농림축산식품부", "산업통상자원부", "보건복지부", "환경부", "고용노동부", "여성가족부",
             "국토교퉁부", "해양수산부", "중소벤처기업부", "국가보훈부", "공정거래위원회", "금융위원회", "국민권익위원회", "개인정보보호위원회",
             "원자력안전위원회", "방송통신위원회", "인사혁신처", "법제처", "식품의약품안전처"]
name_list_chart = ["국조실", "기재부", "교육부", "과기부", "외교부", "통일부", "법무부", "국방부",
                   "행안부", "문체부", "농식품부", "산업부", "복지부", "환경부", "고용부", "여가부",
                   "국토부", "해수부", "중기부", "보훈부", "공정위", "금융위", "권익위", "개보위", "원안위", "방통위", "인사처", "법제처", "식약처"]
number_list = [president_number, prime_number, opm_number, moef_number, moe_number, msit_number, mofa_number, unikorea_number,
               moj_number, mnd_number, mois_number, mcst_number, mafra_number, motie_number, mohw_number, me_number,
               moel_number, mogef_number, molit_number, mof_number, mss_number, mpva_number, ftc_number, fsc_number, acrc_number,
               pipc_number, nssc_number, kcc_number, mpm_number, moleg_number, mfds_number]
number_list_chart = [opm_number, moef_number, moe_number, msit_number, mofa_number, unikorea_number,
               moj_number, mnd_number, mois_number, mcst_number, mafra_number, motie_number, mohw_number, me_number,
               moel_number, mogef_number, molit_number, mof_number, mss_number, mpva_number, ftc_number, fsc_number, acrc_number,
               pipc_number, nssc_number, kcc_number, mpm_number, moleg_number, mfds_number]
department_list = [president, prime, opm, moef, moe, msit, mofa, unikorea,
               moj, mnd, mois, mcst, mafra, motie, mohw, me,
               moel, mogef, molit, mof, mss, mpva, ftc, fsc, acrc, pipc, nssc, kcc, mpm, moleg, mfds]


chart_table = pd.DataFrame([name_list_chart, number_list_chart])
chart_table.rename(columns=chart_table.iloc[0], inplace=True)
chart_table.index = ['name', 'count']
chart_table = chart_table.transpose()
chart_table.drop(chart_table[chart_table['count']==0].index, inplace=True)

bar_chart = go.Bar(x=chart_table['name'], y=chart_table['count'])
fig9 = go.Figure(data=bar_chart)
fig9.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))


########################################################################

with st.container():
    st.subheader(f"{today}")
    st.subheader("")

with st.container():
    st.subheader("기관별 보도량")
    #st.bar_chart(name_number, use_container_width=True)
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown("""---""")

with st.container():
    st.subheader("기관별 주요보도")


col1, col2 = st.columns(2)
n = 1
for name, number, department in zip(name_list, number_list, department_list):
    if number > 0 :
        n = n + 1
        if n % 2 == 0:
            with col1:
                with st.container():
                    with st.expander(f"{name} : {number}건"):
                        st.plotly_chart(department, use_container_width=True)
        else:
            with col2:
                with st.container():
                    with st.expander(f"{name} : {number}건"):
                        st.plotly_chart(department, use_container_width=True)