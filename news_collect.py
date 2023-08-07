print("hello")

import requests
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from tqdm import tqdm, tqdm_notebook
from pytz import timezone
from fake_useragent import UserAgent
from functools import wraps


ua = UserAgent()


# now = datetime.now(timezone('Asia/Seoul'))
# date = now.date()
# date = str(date)
# target_date = re.sub('-', '', date)
target_date = "20230802"

press_numbers = ['032', '005', '020', '021', '081', '022', '023', '025', '028', '469', '009', '011', '366', '015']
press_list = []
url_list = []
title_list = []
date_list = []
body_list = []



def parser(link):
    title = bs.find('h2').get_text()
    #title = bs.select('h2')[0].get_text()
    if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
        pass
    else:
        title_list.append(title)

        press = "경향신문" if i =='032' else "국민일보" if i=="005" else "동아일보" if i=="020" else "문화일보"if i=="021" else "서울신문" if i=="081" else "세계일보" if i=="022" else "조선일보" if i=="023" else "중앙일보" if i=="025" else "한겨레" if i=="028" else "한국일보" if i=="469"else "매일경제" if i=="009" else "서울경제" if i=="011" else "조선비즈" if i=="366" else "한국경제"
        press_list.append(press)
        date_list.append(target_date)

        bodies = bs.find('div', {'id': 'dic_area'})
        if bodies == None:
            bodies == ""
        else :
            bodies = bodies.get_text()
            bodies = re.sub('\n', '', bodies)
            bodies = re.sub('\t', '', bodies)
        body_list.append(bodies)
        url_list.append(link)
        time.sleep(1+random.random()*5)


for i in press_numbers:
    #신문사 첫 페이지 정보 읽기
    Press_URL = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid="+str(i)+"&listType=paper&date="+str(target_date)
    headers = {'User-Agent': ua.random}
    req = requests.get(Press_URL, headers=headers)
    bs = BeautifulSoup(req.text, 'html.parser')

    
    #특정일 페이지 수 확인
    pages = int(len(bs.findAll("a", {"class":"nclicks(cnt_order)"}))/2)


    for page in tqdm(range(1,pages+1)):
        #신문사 내 특정 페이지 호출
        page_url = Press_URL+"&page="+str(page)
        headers = {'User-Agent': ua.random}
        req = requests.get(page_url, headers=headers)
        bs = BeautifulSoup(req.text, 'html.parser')

        #특정 페이지 내 기사목록 추출
        links = []
        if len(bs.select('ul.type13')) != 0:
            ul_tags = bs.select('ul.type13')
            for ul_tag in ul_tags:
                li_tags = ul_tag.select('li')
                for li_tag in li_tags:
                    link = li_tag.a['href']
                    links.append(link)

        ul_tags = bs.select('ul.type02')
        for ul_tag in ul_tags:
            li_tags = ul_tag.select('li')
            for li_tag in li_tags:
                link = li_tag.a['href']
                links.append(link)

        #개별 기사 내 제목,날짜,본문 추출
        for link in links:
            headers = {'User-Agent': ua.random}
            req = requests.get(link, headers=headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            if bs.find('h2') is None:
                now = datetime.now(timezone('Asia/Seoul'))
                now = now.strftime('%y-%m-%d %H %M %S')
                print(f"{now} 연결 끊김. 1차 재시도 예정..")
                time.sleep(200)
                headers = {'User-Agent': ua.random}
                req = requests.get(link, headers=headers)
                bs = BeautifulSoup(req.text, 'html.parser')
                if bs.find('h2') is None:
                    now = datetime.now(timezone('Asia/Seoul'))
                    now = now.strftime('%y-%m-%d %H %M %S')
                    print(f"{now} 연결 끊김. 2차 재시도 예정..")
                    time.sleep(480)
                    headers = {'User-Agent': ua.random}
                    req = requests.get(link, headers=headers)
                    bs = BeautifulSoup(req.text, 'html.parser')
                    parser(link)
                else:
                    parser(link)
                
            else:
                parser(link)

        time.sleep(2+random.random()*4)
    press = "경향신문" if i =='032' else "국민일보" if i=="005" else "동아일보" if i=="020" else "문화일보"if i=="021" else "서울신문" if i=="081" else "세계일보" if i=="022" else "조선일보" if i=="023" else "중앙일보" if i=="025" else "한겨레" if i=="028" else "한국일보" if i=="469"else "매일경제" if i=="009" else "서울경제" if i=="011" else "조선비즈" if i=="366" else "한국경제"
    now = datetime.now(timezone('Asia/Seoul'))
    now = now.strftime('%y-%m-%d %H %M %S')
    print(f"{now} {press} 완료")
    time.sleep(2+random.random()*5)

result = {'Press' : press_list, 'Url' : url_list, 'Title':title_list, 'Date':date_list, 'Body':body_list}
df=pd.DataFrame(result)
df.replace('', np.nan, inplace=True)  #공란은 NaN 처리
df.dropna(inplace=True)               #NaN 포함한 행 제거
pd.to_datetime(df['Date'])            #날짜형식 부여
df.reset_index(drop=True, inplace=True)

previous_df = pd.read_csv('/home/ubuntu/test2/full_result.csv')
del previous_df["Unnamed: 0"]

full_df = pd.concat([previous_df, df])
full_df.reset_index(drop=True, inplace=True)

full_df.to_csv('/home/ubuntu/test2/full_result.csv')
now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} news collect complete")