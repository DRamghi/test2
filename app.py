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
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')

import re

from collections import Counter

import plotly.graph_objects as go


############ KoBert 모델 구현을 위한 환경설정 ###########
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

#transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

#device = torch.device("cuda:0")
device = torch.device('cpu')


##########################################
#페이지 기본설정
st.set_page_config(
    page_title="지면기사 분석",
    layout="wide",
)

###########################################

search_word = "0"
start_date = "0"
end_date = "0"


# with st.sidebar:
#     st.markdown("<h1 style='text-align: center; color: black;'>키워드를 입력하세요</h1>", unsafe_allow_html=True)
#     input1 = st.text_input(label="키워드", placeholder="대한민국")
#     #input2 = st.text_input(label="시작일자", placeholder="2022-11-03")
#     #input3 = st.text_input(label="종료일자", placeholder="2022-11-04")
#     input2 = st.date_input(label="시작일자")
#     input3 = st.date_input(label="종료일자")
#     col5, col6, col7 = st.columns(3)
#     with col5:
#         pass
#     with col6:
#         button = st.button("입력")
#     with col7:
#         pass

with st.sidebar:
    choice = option_menu("지면기사 분석", ["오늘의 주요 보도", "키워드 검색"],
                         icons=['house', 'kanban'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )


#######################################################
file_path = "C:\\github\\test2\\full_result.csv"
@st.cache_data
def load_data():
  data = pd.read_csv(file_path)
  return data



####################################################################
# BERT 모델, Vocabulary 불러오기
bertmodel, vocab = get_pytorch_kobert_model()


# BERT 모델에 들어가기 위한 dataset을 만들어주는 클래스
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i],))

    def __len__(self):
        return (len(self.labels))


# Setting parameters
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 5
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5

tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size=768,
                 num_classes=3,  ##클래스 수 조정##
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                              attention_mask=attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


@st.cache_data
def load_model():
    model = BERTClassifier(bertmodel, dr_rate=0.5).to(device)
    model.load_state_dict(
        torch.load('C:\\github\\project3\\main\\model_state_dict.pt', map_location=device), strict=False)
    return model

model = load_model()


###################################################################
if button:
    search_word = input1
    start_date = str(input2)
    end_date = str(input3)

#################################################################

data = load_data()
data['Date'] = data['Date'].astype('str')
data['Date'] = pd.to_datetime(data['Date'])
data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

if search_word and start_date and end_date != "0":
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    ########## 특정 키워드 빈도수 ##################

    date_data = data[data['Date'].between(start_date, end_date)]  #####대상기간 내 기사 본문 추출

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


    fig1 = px.line(d, x="date", y="count")





    ##########불용어 사전#########################
    stop_words = "이번 담당 여러분 관련 이날 이후 오후 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간"
    stop_words = set(stop_words.split(' '))


    #########특정 키워드 연관어 분석################

    date_list = set(result_list['Date'])
    date_list = list(date_list)
    date_list.sort(reverse=False)
    period = end_date - start_date + timedelta(days=1)
    period = period.days

    keywords_table = pd.DataFrame()
    total_word_list = []
    a = []

    n = int(period / 7) + 1
    for i in range(0, int(period / n)):
        start_day = start_date + timedelta(days=n * i)
        str_start_day = str(start_day)[5:10].replace('-', '.') + " ~"
        end_day = start_date + timedelta(days=n * (i + 1) - 1)
        str_end_day = str(end_day)[5:10].replace('-', '.')

        date_result = result_list[
            result_list['Date'].between(start_day, end_day)]

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

        top_related_words = dict(c.most_common(10))
        if str_start_day == str_end_day:
            first_column = str_end_day
        else: first_column = f'{str_start_day}~{str_end_day}'

        date_top_related_words = pd.DataFrame(list(top_related_words.items()), columns=[first_column, "second"])
        for i in range(0,10):
            date_top_related_words.iloc[i,0] = f'{date_top_related_words.iloc[i,0]}  :  {date_top_related_words.iloc[i,1]}건'
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

        top_related_words = dict(c.most_common(10))

        if str_plus_day == str_plus_alpha_day:
            last_column = str_plus_alpha_day
        else:
            last_column = f'{str_plus_day}~{str_plus_alpha_day}'

        #date_top_related_words = pd.DataFrame(list(top_related_words.items()),
        #                                      columns=[str_plus_day, str_plus_alpha_day])
        #date_top_related_words.index = date_top_related_words.index + 1
        #keywords_table = pd.concat([keywords_table, date_top_related_words], axis=1, join='outer')




        date_top_related_words = pd.DataFrame(list(top_related_words.items()), columns=[last_column, "second"])
        for i in range(0, 10):
            date_top_related_words.iloc[
                i, 0] = f'{date_top_related_words.iloc[i, 0]}  :  {date_top_related_words.iloc[i, 1]}건'
        date_top_related_words.drop(labels='second', axis=1, inplace=True)
        date_top_related_words.index = date_top_related_words.index + 1
        keywords_table = pd.concat([keywords_table, date_top_related_words], axis=1, join='outer')



    c = Counter(total_word_list)
    top_related_words = dict(c.most_common(50))
    wc = WordCloud(background_color='white', font_path='C:\\github\\project2\\main\\NanumGothic.ttf')
    wc.generate_from_frequencies(top_related_words)
    figure = plt.figure(figsize=(width, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    plt.close(figure)

    ###################기사 긍정,부정 분석#####################

    def predict(predict_sentence):

        data = [predict_sentence, '0']
        dataset_another = [data]

        another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
        test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size,
                                                      num_workers=0)  # 원래 num_workers=5였음

        model.eval()

        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)

            valid_length = valid_length
            label = label.long().to(device)

            out = model(token_ids, valid_length, segment_ids)

            test_eval = []
            for i in out:
                logits = i
                logits = logits.detach().cpu().numpy()

                if np.argmax(logits) == 0:
                    test_eval.append("부정")
                elif np.argmax(logits) == 1:
                    test_eval.append("중립")
                elif np.argmax(logits) == 2:
                    test_eval.append("긍정")

            return test_eval[0]


    import re

    pos_list = []
    pos_press_list=[]
    pos_link_list=[]
    neg_list = []
    neg_press_list = []
    neg_link_list = []
    neu_list = []
    neu_press_list = []
    neu_link_list = []

    for i in range(0, len(result_list)):
        title = result_list.iloc[i, 2]
        press = result_list.iloc[i, 0]
        link = result_list.iloc[i, 1]
        title_link = f'''<a href="{link}">{title}</a>'''
        title_score = predict(title)
        if title_score == "긍정":
            pos_list.append(title_link)
            pos_press_list.append(press)
        elif title_score == "부정":
            neg_list.append(title_link)
            neg_press_list.append(press)
        else:
            neu_list.append(title_link)
            neu_press_list.append(press)

    pos_time = len(pos_list)
    neg_time = len(neg_list)
    neu_time = len(neu_list)
    net_time = pos_time + neg_time + neu_time

    pos_table = pd.DataFrame({'제목': pos_list, '언론사' : pos_press_list})
    pos_table.index = pos_table.index + 1



    neg_table = pd.DataFrame({'제목': neg_list, '언론사': neg_press_list})
    neg_table.index = neg_table.index + 1

    neu_table = pd.DataFrame({'제목' : neu_list, '언론사' : neu_press_list})
    neu_table.index = neu_table.index + 1


    #############################

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

    #######################################################################

    with st.container():
        with st.container():
            st.subheader("1.일자별 언급량")
            st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""---""")
        with st.container():
            st.subheader("2.기간별 연관검색어")
            st.dataframe(keywords_table, use_container_width=True)
        st.markdown("""---""")
        with st.container():
            st.subheader("3.Word Cloud")
            st.pyplot(figure)
        st.markdown("""---""")
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


