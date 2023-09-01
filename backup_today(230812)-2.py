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
from pytz import timezone

##########################################
#페이지 기본설정
st.set_page_config(
    page_title="지면기사 분석",
    layout="wide",
)
#######################################################

data = pd.read_csv("/home/ubuntu/test2/today_department_table.csv")
today_data = pd.read_csv("/home/ubuntu/test2/full_result.csv")
del data['Unnamed: 0']
del today_data['Unnamed: 0']


def department_search(search_word): #날짜는 2022-11-10 형식으로 입력
  department_data = data[data['department']==search_word]
  department_title = department_data['title']
  pos_time = len(department_data[department_data['sentiment']=="긍정"])
  neg_time = len(department_data[department_data['sentiment']=="부정"])
  neu_time = len(department_data[department_data['sentiment']=="중립"])
  pos_title = department_data[department_data['sentiment']=="긍정"]['title']
  neg_title = department_data[department_data['sentiment']=="부정"]['title']
  neu_title = department_data[department_data['sentiment']=="중립"]['title']

  fig_pos = go.Figure(
      data=[
          go.Table(
              header=dict(
                  values=[f"<b>긍정보도</b>"],
                  # fill_color='blue'
              ),
              cells=dict(
                  values=[pos_title],
                  align="left"
              )
          )
      ]
  )
  fig_neg = go.Figure(
      data=[
          go.Table(
              header=dict(
                  values=[f"<b>부정보도</b>"],
                  # fill_color='blue'
              ),
              cells=dict(
                  values=[neg_title],
                  align="left"
              )
          )
      ]
  )
  fig_neu = go.Figure(
      data=[
          go.Table(
              header=dict(
                  values=[f"<b>중립보도</b>"],
                  # fill_color='blue'
              ),
              cells=dict(
                  values=[neu_title],
                  align="left"
              )
          )
      ]
  )
  fig_pos.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))
  fig_neg.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))
  fig_neu.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

  return pos_time, neg_time, neu_time, fig_pos, fig_neg, fig_neu



now = datetime.now(timezone('Asia/Seoul'))
today = str(now.date())

today2 = re.sub('-', '', today)
today2 = int(today2)


if data['date'][0] != today2:
    message1 = "아직 오늘 보도가 업데이트되지 않아 전일 보도를 제공합니다." 
    message2 = "보도는 매일 아침 8시경 업데이트됩니다."
    today = now - timedelta(days=1)
    today = str(today.date())
    today2 = re.sub('-', '', today)
    today2 = int(today2)
     
else:
    message1 =""
    message2 =""


president_pos, president_neg, president_neu, president_fig_pos, president_fig_neg, president_fig_neu = department_search("대통령비서실")
prime_pos, prime_neg, prime_neu, prime_fig_pos, prime_fig_neg, prime_fig_neu = department_search("총리")
opm_pos, opm_neg, opm_neu, opm_fig_pos, opm_fig_neg, opm_fig_neu = department_search("국무조정실")
moef_pos, moef_neg, moef_neu, moef_fig_pos, moef_fig_neg, moef_fig_neu = department_search("기획재정부")
moe_pos, moe_neg, moe_neu, moe_fig_pos, moe_fig_neg, moe_fig_neu = department_search("교육부")
msit_pos, msit_neg, msit_neu, msit_fig_pos, msit_fig_neg, msit_fig_neu = department_search("과학기술정보통신부")
mofa_pos, mofa_neg, mofa_neu, mofa_fig_pos, mofa_fig_neg, mofa_fig_neu = department_search("외교부")
unikorea_pos, unikorea_neg, unikorea_neu, unikorea_fig_pos, unikorea_fig_neg, unikorea_fig_neu = department_search("통일부")
moj_pos, moj_neg, moj_neu, moj_fig_pos, moj_fig_neg, moj_fig_neu = department_search("법무부")
mnd_pos, mnd_neg, mnd_neu, mnd_fig_pos, mnd_fig_neg, mnd_fig_neu = department_search("국방부")
mois_pos, mois_neg, mois_neu, mois_fig_pos, mois_fig_neg, mois_fig_neu = department_search("행정안전부")
mcst_pos, mcst_neg, mcst_neu, mcst_fig_pos, mcst_fig_neg, mcst_fig_neu = department_search("문화체육관광부")
mafra_pos, mafra_neg, mafra_neu, mafra_fig_pos, mafra_fig_neg, mafra_fig_neu = department_search("농림축산식품부")
motie_pos, motie_neg, motie_neu, motie_fig_pos, motie_fig_neg, motie_fig_neu = department_search("산업통상자원부")
mohw_pos, mohw_neg, mohw_neu, mohw_fig_pos, mohw_fig_neg, mohw_fig_neu = department_search("보건복지부")
me_pos, me_neg, me_neu, me_fig_pos, me_fig_neg, me_fig_neu = department_search("환경부")
moel_pos, moel_neg, moel_neu, moel_fig_pos, moel_fig_neg, moel_fig_neu = department_search("고용노동부")
mogef_pos, mogef_neg, mogef_neu, mogef_fig_pos, mogef_fig_neg, mogef_fig_neu = department_search("여성가족부")
molit_pos, molit_neg, molit_neu, molit_fig_pos, molit_fig_neg, molit_fig_neu = department_search("국토교통부")
mof_pos, mof_neg, mof_neu, mof_fig_pos, mof_fig_neg, mof_fig_neu = department_search("해양수산부")
mss_pos, mss_neg, mss_neu, mss_fig_pos, mss_fig_neg, mss_fig_neu = department_search("중소벤처기업부")
mpva_pos, mpva_neg, mpva_neu, mpva_fig_pos, mpva_fig_neg, mpva_fig_neu = department_search("국가보훈부")
ftc_pos, ftc_neg, ftc_neu, ftc_fig_pos, ftc_fig_neg, ftc_fig_neu = department_search("공정거래위원회")
fsc_pos, fsc_neg, fsc_neu, fsc_fig_pos, fsc_fig_neg, fsc_fig_neu = department_search("금융위원회")
acrc_pos, acrc_neg, acrc_neu, acrc_fig_pos, acrc_fig_neg, acrc_fig_neu = department_search("국민권익위원회")
pipc_pos, pipc_neg, pipc_neu, pipc_fig_pos, pipc_fig_neg, pipc_fig_neu = department_search("개인정보보호위원회")
nssc_pos, nssc_neg, nssc_neu, nssc_fig_pos, nssc_fig_neg, nssc_fig_neu = department_search("원자력안전위원회")
kcc_pos, kcc_neg, kcc_neu, kcc_fig_pos, kcc_fig_neg, kcc_fig_neu = department_search("방송통신위원회")
mpm_pos, mpm_neg, mpm_neu, mpm_fig_pos, mpm_fig_neg, mpm_fig_neu = department_search("인사혁신처")
moleg_pos, moleg_neg, moleg_neu, moleg_fig_pos, moleg_fig_neg, moleg_fig_neu = department_search("법제처")
mfds_pos, mfds_neg, mfds_neu, mfds_fig_pos, mfds_fig_neg, mfds_fig_neu = department_search("식품의약품안전처")



name_list = ["대통령비서실", "국무총리", "국무조정실", "기획재정부", "교육부", "과학기술정보통신부", "외교부", "통일부", "법무부", "국방부",
             "행정안전부", "문화체육관광부", "농림축산식품부", "산업통상자원부", "보건복지부", "환경부", "고용노동부", "여성가족부",
             "국토교통부", "해양수산부", "중소벤처기업부", "국가보훈부", "공정거래위원회", "금융위원회", "국민권익위원회", "개인정보보호위원회",
             "원자력안전위원회", "방송통신위원회", "인사혁신처", "법제처", "식품의약품안전처"]
name_list_chart = ["국조실", "기재부", "교육부", "과기부", "외교부", "통일부", "법무부", "국방부",
                   "행안부", "문체부", "농식품부", "산업부", "복지부", "환경부", "고용부", "여가부",
                   "국토부", "해수부", "중기부", "보훈부", "공정위", "금융위", "권익위", "개보위", "원안위", "방통위", "인사처", "법제처", "식약처"]

#number_list_chart = [opm_number, moef_number, moe_number, msit_number, mofa_number, unikorea_number,
#               moj_number, mnd_number, mois_number, mcst_number, mafra_number, motie_number, mohw_number, me_number,
#               moel_number, mogef_number, molit_number, mof_number, mss_number, mpva_number, ftc_number, fsc_number, acrc_number,
#               pipc_number, nssc_number, kcc_number, mpm_number, moleg_number, mfds_number]

#number_list = [president_number, prime_number, opm_number, moef_number, moe_number, msit_number, mofa_number, unikorea_number,
#               moj_number, mnd_number, mois_number, mcst_number, mafra_number, motie_number, mohw_number, me_number,
#               moel_number, mogef_number, molit_number, mof_number, mss_number, mpva_number, ftc_number, fsc_number, acrc_number,
#               pipc_number, nssc_number, kcc_number, mpm_number, moleg_number, mfds_number]

# department_list = [president, prime, opm, moef, moe, msit, mofa, unikorea,
#                moj, mnd, mois, mcst, mafra, motie, mohw, me,
#                moel, mogef, molit, mof, mss, mpva, ftc, fsc, acrc, pipc, nssc, kcc, mpm, moleg, mfds]

pos_list = [opm_pos, moef_pos, moe_pos, msit_pos, mofa_pos, unikorea_pos,
               moj_pos, mnd_pos, mois_pos, mcst_pos, mafra_pos, motie_pos, mohw_pos, me_pos,
               moel_pos, mogef_pos, molit_pos, mof_pos, mss_pos, mpva_pos, ftc_pos, fsc_pos, acrc_pos,
               pipc_pos, nssc_pos, kcc_pos, mpm_pos, moleg_pos, mfds_pos]

plus_pos_list = [president_pos, prime_pos]
plus_pos_list = plus_pos_list + pos_list


neg_list = [opm_neg, moef_neg, moe_neg, msit_neg, mofa_neg, unikorea_neg,
               moj_neg, mnd_neg, mois_neg, mcst_neg, mafra_neg, motie_neg, mohw_neg, me_neg,
               moel_neg, mogef_neg, molit_neg, mof_neg, mss_neg, mpva_neg, ftc_neg, fsc_neg, acrc_neg,
               pipc_neg, nssc_neg, kcc_neg, mpm_neg, moleg_neg, mfds_neg]
               
plus_neg_list = [president_neg, prime_neg]
plus_neg_list = plus_neg_list + neg_list

neu_list = [opm_neu, moef_neu, moe_neu, msit_neu, mofa_neu, unikorea_neu,
               moj_neu, mnd_neu, mois_neu, mcst_neu, mafra_neu, motie_neu, mohw_neu, me_neu,
               moel_neu, mogef_neu, molit_neu, mof_neu, mss_neu, mpva_neu, ftc_neu, fsc_neu, acrc_neu,
               pipc_neu, nssc_neu, kcc_neu, mpm_neu, moleg_neu, mfds_neu]

plus_neu_list = [president_neu, prime_neu]
plus_neu_list = plus_neu_list + neu_list

fig_pos_list = [president_fig_pos, prime_fig_pos, opm_fig_pos, moef_fig_pos, moe_fig_pos, msit_fig_pos, mofa_fig_pos, unikorea_fig_pos,
               moj_fig_pos, mnd_fig_pos, mois_fig_pos, mcst_fig_pos, mafra_fig_pos, motie_fig_pos, mohw_fig_pos, me_fig_pos,
               moel_fig_pos, mogef_fig_pos, molit_fig_pos, mof_fig_pos, mss_fig_pos, mpva_fig_pos, ftc_fig_pos, fsc_fig_pos, acrc_fig_pos,
               pipc_fig_pos, nssc_fig_pos, kcc_fig_pos, mpm_fig_pos, moleg_fig_pos, mfds_fig_pos]

fig_neg_list = [president_fig_neg, prime_fig_neg, opm_fig_neg, moef_fig_neg, moe_fig_neg, msit_fig_neg, mofa_fig_neg, unikorea_fig_neg,
               moj_fig_neg, mnd_fig_neg, mois_fig_neg, mcst_fig_neg, mafra_fig_neg, motie_fig_neg, mohw_fig_neg, me_fig_neg,
               moel_fig_neg, mogef_fig_neg, molit_fig_neg, mof_fig_neg, mss_fig_neg, mpva_fig_neg, ftc_fig_neg, fsc_fig_neg, acrc_fig_neg,
               pipc_fig_neg, nssc_fig_neg, kcc_fig_neg, mpm_fig_neg, moleg_fig_neg, mfds_fig_neg]

fig_neu_list = [president_fig_neu, prime_fig_neu, opm_fig_neu, moef_fig_neu, moe_fig_neu, msit_fig_neu, mofa_fig_neu, unikorea_fig_neu,
               moj_fig_neu, mnd_fig_neu, mois_fig_neu, mcst_fig_neu, mafra_fig_neu, motie_fig_neu, mohw_fig_neu, me_fig_neu,
               moel_fig_neu, mogef_fig_neu, molit_fig_neu, mof_fig_neu, mss_fig_neu, mpva_fig_neu, ftc_fig_neu, fsc_fig_neu, acrc_fig_neu,
               pipc_fig_neu, nssc_fig_neu, kcc_fig_neu, mpm_fig_neu, moleg_fig_neu, mfds_fig_neu]

number_list = [president_pos + president_neg + president_neu, prime_pos + prime_neg + prime_neu]
for i in range(0, len(pos_list)):
    a = pos_list[i] + neg_list[i] + neu_list[i]
    number_list.append(a)

chart_table_pos = pd.DataFrame([name_list_chart, pos_list])
chart_table_pos = chart_table_pos.transpose()
chart_table_pos['sentiment'] = "긍정"
chart_table_neg = pd.DataFrame([name_list_chart, neg_list])
chart_table_neg = chart_table_neg.transpose()
chart_table_neg['sentiment'] = "부정"

chart_table_neu = pd.DataFrame([name_list_chart, neu_list])
chart_table_neu = chart_table_neu.transpose()
chart_table_neu['sentiment'] = "중립"


chart_table = pd.concat([chart_table_pos, chart_table_neu, chart_table_neg])
  #chart_table.rename(columns=chart_table.iloc[0], inplace=True)
chart_table_list = list(chart_table.columns)
chart_table_list[0] = 'department'
chart_table_list[1] = 'count'
chart_table_list[2] = 'sentiment'
chart_table.columns = chart_table_list

chart_table = chart_table[chart_table['count'] != 0]

fig9 = px.bar(chart_table, x='department', y='count', color='sentiment')


########################################################################

with st.container():
    st.subheader(f"{today} 주요 보도")
    st.text(message1)
    st.text(message2)
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
for name, number, pos, neg, neu, fig_pos, fig_neg, fig_neu in zip(name_list, number_list, plus_pos_list, plus_neg_list, plus_neu_list, fig_pos_list, fig_neg_list, fig_neu_list):
    if number > 0 :
        n = n + 1
        if n % 2 == 0:
            with col1:
                with st.container():
                    with st.expander(f"{name} : {number}건"):
                        if pos > 0:
                            st.plotly_chart(fig_pos, use_container_width=True)
                        if neg > 0:
                            st.plotly_chart(fig_neg, use_container_width=True)
                        if neu > 0:
                            st.plotly_chart(fig_neu, use_container_width=True)
        else:
            with col2:
                with st.container():
                    with st.expander(f"{name} : {number}건"):
                        if pos > 0:
                            st.plotly_chart(fig_pos, use_container_width=True)
                        if neg > 0:
                            st.plotly_chart(fig_neg, use_container_width=True)
                        if neu > 0:
                            st.plotly_chart(fig_neu, use_container_width=True)

##오늘의 키워드 워드클라우드

# st.markdown("""---""")
# with st.container():
#         st.subheader("오늘의 주요 키워드")


# today_data = today_data[today_data['Date']==today2]
# text = []
# for body in today_data['Body']:
#     lines = body.split(".")
#     text = text + lines[0:5]

# stop_words = "한국 서울 대표 이번 담당 오늘 여러분 관련 이날 이후 오후 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간 우리 외부 국가 계기 구성 현장 그날 참석 계획 시일 의견 수렴 검토 요청 이유 논의 과정 결정 의미 확정 사업 회의 사건 조성 주변 사람 상태 누군가 정도 이곳 일대 당시 동안 마련 근처 정도 느낌 소식 그곳 이곳 이상"
# stop_words = set(stop_words.split(' '))

# noun_list = []
# print("mecab 실행")
# for line in text:
#     print(line)
#     nouns = mecab.nouns(line)
#     for noun in nouns:
#         if len(noun) > 1 and noun not in stop_words :
#             noun_list.append(noun)  
# print("mecab 종료")

# c = Counter(noun_list)
# top_related_words = dict(c.most_common(50))
# wc = WordCloud(background_color='white', font_path='NanumGothic.ttf')
# wc.generate_from_frequencies(top_related_words)
# figure = plt.figure(figsize= (5, 5))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis('off')
# plt.show()
# plt.close(figure)


# with st.container():
#         st.pyplot(figure)
    

