
############ KoBert 모델 구현을 위한 환경설정 ###########
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

import sys
sys.path.append("/home/ubuntu/KoBERT")

#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

#transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

#device = torch.device("cuda:0")
device = torch.device('cpu')


################################

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
        torch.load("model_state_dict.pt", map_location=device), strict=False)
    return model

model = load_model()


###############

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