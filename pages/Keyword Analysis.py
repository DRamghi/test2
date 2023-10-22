import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np
import math

import matplotlib
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


###########################################

search_word = "0"
start_date = "0"
end_date = "0"

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        input1 = st.text_input(label="키워드", placeholder="대한민국")
    with col2:
        input2 = st.date_input(label="시작일자")
        st.text("*2023년 7월 5일부터 검색 가능")
    with col3:
        input3 = st.date_input(label="종료일자")
    with col4:
        st.write("")
        st.write("")
        button = st.button("입력")


#######################################################
file_path = "/home/ubuntu/test2/full_result.csv" 
@st.cache_data
def load_data():
  data = pd.read_csv(file_path)
  return data

####################################################################


data = load_data()
data['Date'] = data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])
data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

days = ['월', '화', '수', '목', '금', '토', '일']

###################################################################
if button:
    search_word = input1
    start_date = str(input2)
    end_date = str(input3)

#################################################################



if search_word and start_date and end_date != "0":
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    ########## 특정 키워드 빈도수 ##################

    date_data = data[data['Date'].between(start_date, end_date)]  #####대상기간 내 기사 본문 추출


    # 특정 키워드 기사 index 추출(제목에 포함 or 본문에 1번 이상 포함)
    # 검색날짜 범위 중 일요일을 제외한 날짜 리스트 만들기
    full_date_list = pd.date_range(start=start_date, end=end_date)
    week_day_list = []
    for i in full_date_list:
        if days[datetime.date(i).weekday()] != "일":
            week_day_list.append(i)
    full_date_list = week_day_list

    count_list = []
    table = pd.DataFrame()
    index_list = []
    date_list = []
    for i in full_date_list:
        a = date_data[date_data['Date'] == i]
        count = 0
        pos_count = 0
        neg_count = 0
        neu_count = 0
        for j in range(0, len(a)):
            title_j = a.iloc[j, 2]
            body_j = a.iloc[j, 4]
            if title_j.count(search_word) > 0 or body_j.count(search_word) > 2:
                count = count + 1
                index_list.append(a.index[j])
                if date_list.count(i) == 0:
                    date_list.append(i)
                if a.iloc[j,5] == "긍정":
                    pos_count = pos_count + 1
                elif a.iloc[j,5] == "부정":
                    neg_count = neg_count + 1
                else:
                    neu_count = neu_count + 1
        count_list.append(count)
        new = {'날짜' : [i, i, i], '논조' : ['총 건수', '긍정', '부정'], '보도건수' : [count, pos_count, neg_count]}
        new = pd.DataFrame(data=new)
        table = pd.concat([table, new])

    d = table

    fig1 = px.line(d, x="날짜", y="보도건수", color="논조", height=400, render_mode='svg')
    #fig1 = px.line(d, x="날짜", y="언급량", color="논조", height=400, render_mode='svg')
    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))
    fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor='center', x=0.5))
    fig1.update_layout(legend_title_text="")
    fig1.update_xaxes(
        rangebreaks=[
            dict(bounds=["sun", "mon"]) #hide weekends
        ]
    )
    

    with st.container():
        st.subheader("1.일자별 보도건수")
        st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""---""")


    ##########불용어 사전#########################
    stop_words = "이번 담당 여러분 관련 이날 이달 개월 이후 오후 오전 경우 기간 때문 당시 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간 지난달 이유 다음"
    stop_words = set(stop_words.split(' '))





    #########특정 키워드 연관어 분석(테스트(절대적 빈도))################

    result_list = date_data.loc[index_list]
    date_list.sort(reverse=False)

    period = end_date - start_date + timedelta(days=1)
    period = period.days

    keywords_table = pd.DataFrame()
    total_word_list = []
    a = []

    n = int(period / 7) + 1
    for i in range(0, int(period / n)):
        start_day = start_date + timedelta(days=n * i)
        if start_day > end_date :
            break
        else:
            str_start_day = str(start_day)[5:10].replace('-', '.') + "~"
            end_day = start_date + timedelta(days=n * (i + 1) - 1)
            str_end_day = str(end_day)[5:10].replace('-', '.')

            date_result = result_list[
                result_list['Date'].between(start_day, end_day)]

            if len(date_result) == 0:
                pass
            else:
                text = '\n'.join(date_result['Body'])
                lines = text.split(".")

                # 명사 추출
                words_list = []
                for line in lines:
                    if search_word in line:
                        nouns = mecab.nouns(line)
                        for noun in nouns:
                            if len(noun) > 1 and noun not in stop_words and noun != search_word:
                                words_list.append(noun)  # 한 문장에서 명사들만 추출(일자별)
                                total_word_list.append(noun)  # 한 문장에서 명사들만 추출(전 기간)

                #bigram
                for j in range(len(words_list)-1):
                    words_list.append(f"{words_list[j]} {words_list[j+1]}")

                c = Counter(words_list)

                if str_start_day == str_end_day:
                    top_related_words = {"date" : f'{str_end_day}'}
                else:
                    top_related_words = {"date" : f'{str_start_day}{str_end_day}'}
                top_related_words.update(dict(c.most_common(20)))
                a.append(top_related_words)

    if period % n == 0:
        pass
    else:
        plus_day = start_date + timedelta(days=(n * (i + 1)))
        str_plus_day = str(plus_day)[5:10].replace('-', '.') + "~"
        plus_alpha_day = start_date + timedelta(days=(n * (i + 1)) + period % n -1)
        str_plus_alpha_day = str(plus_alpha_day)[5:10].replace('-', '.')
        date_result = result_list[result_list['Date'].between(plus_day, plus_alpha_day)]

        if len(date_result) == 0:
            pass
        else:
            text = '\n'.join(date_result['Body'])
            lines = text.split(".")

            # 명사 추출
            words_list = []
            for line in lines:
                if search_word in line:
                    nouns = mecab.nouns(line)
                    for noun in nouns:
                        if len(noun) > 1 and noun not in stop_words and noun != search_word:
                            words_list.append(noun)  # 한 문장에서 명사들만 추출(일자별)
                            total_word_list.append(noun)  # 한 문장에서 명사들만 추출(전 기간)

            #bigram
            for j in range(len(words_list)-1):
                words_list.append(f"{words_list[j]} {words_list[j+1]}")
            
            c = Counter(words_list)

            if str_plus_day == str_plus_alpha_day:
                top_related_words = {"date" : f'{str_plus_alpha_day}'}
            else:
                top_related_words = {"date" : f'{str_plus_day}{str_plus_alpha_day}'}
            top_related_words.update(dict(c.most_common(20)))
            a.append(top_related_words)

    most_common_key = []
    for key in list(a[0])[1:16]:
        count = 0
        for i in range(1,len(a)):
            if key in list(a[i])[1:16]:
                include = 1
            else:
                include = 0
            count = count + include
        if count >= len(a)-1:   # 몇개 기간에 포함시 키워드 삭제할지 조정 가능
            most_common_key.append(key)

    for i in range(0,len(a)):
        for key in most_common_key:
            del a[i][key]

    keywords_table = pd.DataFrame()
    for col in a:
        date = col['date']
        del col['date']
        b = pd.DataFrame(list(col.items()), columns=[date, "date"])
        if len(b) >10:
            b = b[0:10]
        else:
            pass

        for i in range(0, len(b)):
            b.iloc[i, 0] = f'{b.iloc[i, 0]}  :  {b.iloc[i, 1]}건'
        b.drop(labels='date', axis=1, inplace=True)
        b.index = b.index + 1

        keywords_table = pd.concat([keywords_table, b], axis=1, join='outer')
    
    most_df = keywords_table




    # c = Counter(total_word_list)
    # if len(c) < 30:
    #     pass
    # else :
    #     word_cloud_message = ""
    #     top_related_words = dict(c.most_common(50))
    #     wc = WordCloud(background_color='white', font_path='NanumGothic.ttf')
    #     wc.generate_from_frequencies(top_related_words)
    #     figure = plt.figure(figsize= (5, 5))
    #     plt.imshow(wc, interpolation='bilinear')
    #     plt.axis('off')
    #     plt.show()
    #     plt.close(figure)

    #######################################################################

    with st.container():
        st.subheader("2.기간별 연관 이슈 키워드")
        st.dataframe(most_df, use_container_width=True, height = 400)
        st.write(f"전 기간 상위 연관 키워드 : {most_common_key}")
    st.markdown("""---""")


    # with st.container():
    #     st.subheader("3.Word Cloud")
    #     if len(c) < 30:
    #         st.write("관련 검색어가 적어 워드클라우드를 생성하지 않습니다")
    #     else:
    #         st.pyplot(figure)
    # st.markdown("""---""")


    ###################기사 긍정,부정 분석#####################

    import re

    pos_list = []
    pos_press_list=[]
    pos_date_list = []
    pos_link_list=[]
    neg_list = []
    neg_press_list = []
    neg_date_list = []
    neg_link_list = []
    neu_list = []
    neu_press_list = []
    neu_date_list = []
    neu_link_list = []

    for i in range(0, len(result_list)):
        title = result_list.iloc[i, 2]
        date = str(result_list.iloc[i, 3])[:-8]
        link = result_list.iloc[i, 1]
        press = result_list.iloc[i, 0]
        title_link = f'''<a href="{link}">{title} ({press})</a>'''
        title_score = result_list.iloc[i,5]   
        if title_score == "긍정":
            pos_list.append(title_link)
            pos_date_list.append(date)
        elif title_score == "부정":
            neg_list.append(title_link)
            neg_date_list.append(date)
        else:
            neu_list.append(title_link)
            neu_date_list.append(date)

    pos_time = len(pos_list)
    neg_time = len(neg_list)
    neu_time = len(neu_list)
    net_time = pos_time + neg_time + neu_time

    pos_table = pd.DataFrame({'제목': pos_list, '날짜' : pos_date_list})
    pos_table = pos_table.sort_values(by=['날짜'])
    pos_table.index = pos_table.index + 1


    neg_table = pd.DataFrame({'제목': neg_list, '날짜' : neg_date_list})
    neg_table = neg_table.sort_values(by=['날짜'])
    neg_table.index = neg_table.index + 1

    neu_table = pd.DataFrame({'제목': neu_list, '날짜' : neu_date_list})
    neu_table = neu_table.sort_values(by=['날짜'])
    neu_table.index = neu_table.index + 1


    #############################

    # if len(pos_table) == 0:
    #     height_pos = 10
    # elif len(pos_table) < 3:
    #     height_pos = len(pos_table) * 70
    # else:
    #     height_pos = len(pos_table) * 50

    # if len(neu_table) == 0:
    #     height_neu = 10
    # elif len(neu_table) < 3:
    #     height_neu = len(neu_table) * 70
    # else:
    #     height_neu = len(neu_table) * 50

    # if len(neg_table) == 0:
    #     height_neg = 10
    # elif len(neg_table) < 3:
    #     height_neg = len(neg_table) * 70
    # else:
    #     height_neg = len(neg_table) * 50


    fig2 = go.Figure(
        data=[
            go.Table(
                columnwidth=[3, 1],
                header=dict(
                    values=[f"<b>{i}</b>" for i in pos_table.columns.to_list()],
                    #fill_color='blue'
                ),
                cells=dict(
                    values=pos_table.transpose(),
                    align="left"
                )
            )
        ]
    )
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

    fig3 = go.Figure(
        data=[
            go.Table(
                columnwidth=[3, 1],
                header=dict(
                    values=[f"<b>{i}</b>" for i in neg_table.columns.to_list()],
                    #fill_color='blue'
                ),
                cells=dict(
                    values=neg_table.transpose(),
                    align="left"
                )
            )
        ]
    )
    fig3.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

    fig4 = go.Figure(
        data=[
            go.Table(
                columnwidth=[3, 1],
                header=dict(
                    values=[f"<b>{i}</b>" for i in neu_table.columns.to_list()],
                    # fill_color='blue'
                ),
                cells=dict(
                    values=neu_table.transpose(),
                    align="left"
                )
            )
        ]
    )
    fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))
#########################

    with st.container():
        st.subheader(f"4.긍정보도 : {net_time}건 중 {pos_time}건")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""---""")
    with st.container():
        st.subheader(f"5.부정보도 : {net_time}건 중 {neg_time}건")
        st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""---""")
    with st.container():
        st.subheader(f"6.중립보도 : {net_time}건 중 {neu_time}건")
        st.plotly_chart(fig4, use_container_width=True)