import pandas as pd

############ KoBert 모델 구현을 위한 환경설정 ###########
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
from pytz import timezone
import time
from datetime import datetime, timedelta

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

now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} cached 모델 불러오기 시작")


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

now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} 모델 불러오기 시작")

#@st.cache_data
def load_model():
    model = BERTClassifier(bertmodel, dr_rate=0.5).to(device)
    model.load_state_dict(
        torch.load("/home/ubuntu/test2/model_state_dict.pt", map_location=device), strict=False)
    return model

model = load_model()

now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} 모델 불러오기 성공")

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


file_path = "/home/ubuntu/test2/full_result.csv"
data = pd.read_csv(file_path)

#################################################################.

data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

for i in tqdm(range(0, len(data))):
    senti = data.iloc[i,5]
    if pd.isna(senti) == True:
        title = data.iloc[i,2]
        data.iloc[i,5] = predict(title)

data.to_csv("/home/ubuntu/test2/full_result.csv")
now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} 완료")
