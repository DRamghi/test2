import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import time
import random
from tqdm import tqdm, tqdm_notebook
from pytz import timezone
from datetime import datetime, timedelta

ua = UserAgent()

data = pd.read_csv('/home/ubuntu/test2/full_result.csv')

del data["Unnamed: 0"]

def raw_webdata(link, referer_random):
    headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': referer_random,
            'Accept-Encoding': 'gzip, deflate, br', 
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
            }
    req = requests.get(link, headers=headers)
    bs = BeautifulSoup(req.text, 'html.parser')
    return bs


def body_extract(bs):
    bodies = bs.find('article', {'id': 'dic_area'})
    if bodies == None:
        bodies == ""
    else :
        bodies = bodies.get_text()
        bodies = re.sub('\n', '', bodies)
        bodies = re.sub('\t', '', bodies)
    time.sleep(2+random.random()*8)
    return bodies

now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} 기사본문 추출 시작")
    
n = 1

for i in tqdm(range(0, len(data))):
    body = data.iloc[i,4]
    if pd.isna(body) == True:
        press = data.iloc[i,0]
        date = data.iloc[i,3]
        date = re.sub('-','',date)
        presscode = "032" if i =='경향신문' else "005" if i=="국민일보" else "020" if i=="동아일보" else "081" if i=="서울신문" else "022" if i=="세계일보" else "023" if i=="조선일보" else "025" if i=="중앙일보" else "028" if i=="한겨레" else "469" if i=="한국일보" else "009" if i=="매일경제" else "011" if i=="서울경제" else "366" if i=="조선비즈" else "015"
        
        referer_list = ["https://news.naver.com/", "https://www.naver.com/", "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid="+presscode, "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=015&listType=paper&date="+date]
        referer_random = random.choice(referer_list)
        link = data.iloc[i,1]
        bs = raw_webdata(link, referer_random)
        if bs.find('article', {'id': 'dic_area'}) is None:
            now = datetime.now(timezone('Asia/Seoul'))
            now = now.strftime('%y-%m-%d %H %M %S')
            print(f"{now} 연결 끊김. {n}차 재시도 예정..")
            n = n+1
            time.sleep(200)
            referer_random = random.choice(referer_list)
            bs = raw_webdata(link, referer_random)
            data.iloc[i,4] = body_extract(bs)
        else:
            data.iloc[i,4] = body_extract(bs)



data.to_csv('/home/ubuntu/test2/full_result2.csv')

now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} 기사본문 추출 완료")