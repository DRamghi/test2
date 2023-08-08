import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np

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
        st.text("*2023년 7월 3일부터 검색 가능")
    with col3:
        input3 = st.date_input(label="종료일자")
    with col4:
        st.write("")
        st.write("")
        button = st.button("입력")


#######################################################
file_path = "full_result.csv"
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
    full_date_list = pd.date_range(start=start_date, end=end_date)

    count_list = []
    index_list = []
    date_list = []
    for i in full_date_list:
        a = date_data[date_data['Date'] == i]
        count = 0
        for j in range(0, len(a)):
            title_j = a.iloc[j, 2]
            body_j = a.iloc[j, 4]
            if title_j.count(search_word) > 0 or body_j.count(search_word) > 0:
                count = count + title_j.count(search_word) + body_j.count(search_word)
                index_list.append(a.index[j])
                if date_list.count(i) == 0:
                    date_list.append(i)
        count_list.append(count)
    d = pd.DataFrame([full_date_list, count_list])
    d = d.transpose()  # 행 열 전환
    d.rename(columns={0: "date"}, inplace=True)
    d.rename(columns={1: "count"}, inplace=True)

    fig1 = px.line(d, x="date", y="count")
    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0, pad=0))

    with st.container():
        st.subheader("1.일자별 언급량")
        st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""---""")


    ##########불용어 사전#########################
    stop_words = "이번 담당 여러분 관련 이날 이후 오후 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간"
    stop_words = set(stop_words.split(' '))





    #########특정 키워드 연관어 분석################

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
            str_start_day = str(start_day)[5:10].replace('-', '.') + " ~"
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

                c = Counter(words_list)

                top_related_words = dict(c.most_common(15))
                if str_start_day == str_end_day:
                    first_column = str_end_day
                else: first_column = f'{str_start_day}~{str_end_day}'

                date_top_related_words = pd.DataFrame(list(top_related_words.items()), columns=[first_column, "second"])
                for d in range(0,15):
                    date_top_related_words.iloc[d,0] = f'{date_top_related_words.iloc[d,0]}  :  {date_top_related_words.iloc[d,1]}건'
                date_top_related_words.drop(labels='second', axis=1, inplace=True)
                date_top_related_words.index = date_top_related_words.index + 1
                keywords_table = pd.concat([keywords_table, date_top_related_words], axis=1, join='outer')

    if period % n == 0:
        pass
    else:
        plus_day = start_date + timedelta(days=(n * (i + 1)))
        str_plus_day = str(plus_day)[5:10].replace('-', '.') + " ~"
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

            c = Counter(words_list)

            top_related_words = dict(c.most_common(15))

            if str_plus_day == str_plus_alpha_day:
                last_column = str_plus_alpha_day
            else:
                last_column = f'{str_plus_day}~{str_plus_alpha_day}'

            date_top_related_words = pd.DataFrame(list(top_related_words.items()), columns=[last_column, "second"])

            for i in range(0, 15):
                date_top_related_words.iloc[i, 0] = f'{date_top_related_words.iloc[i, 0]}  :  {date_top_related_words.iloc[i, 1]}건'
            date_top_related_words.drop(labels='second', axis=1, inplace=True)
            date_top_related_words.index = date_top_related_words.index + 1
            keywords_table = pd.concat([keywords_table, date_top_related_words], axis=1, join='outer')



    c = Counter(total_word_list)
    top_related_words = dict(c.most_common(50))
    wc = WordCloud(background_color='white', font_path='NanumGothic.ttf')
    wc.generate_from_frequencies(top_related_words)
    figure = plt.figure(figsize= (5, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    plt.close(figure)

    #######################################################################

    with st.container():
        st.subheader("2.기간별 연관검색어")
        st.dataframe(keywords_table, use_container_width=True)
    st.markdown("""---""")


    with st.container():
        st.subheader("3.Word Cloud")
        st.pyplot(figure)
    st.markdown("""---""")



