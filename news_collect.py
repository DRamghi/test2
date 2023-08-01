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
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}


now = datetime.now(timezone('Asia/Seoul'))
date = now.date()
date = str(date)
target_date = re.sub('-', '', date)


press_numbers = ['032', '005', '020', '021', '081', '022', '023', '025', '028', '469', '009', '011', '366', '015']
press_list = []
url_list = []
title_list = []
date_list = []
body_list = []
for i in press_numbers:
    #신문사 첫 페이지 정보 읽기
    Press_URL = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid="+str(i)+"&listType=paper&date="+str(target_date)
    req = requests.get(Press_URL, headers=headers)
    bs = BeautifulSoup(req.text, 'html.parser')

    #특정일 페이지 수 확인
    pages = int(len(bs.findAll("a", {"class":"nclicks(cnt_order)"}))/2)


    for page in tqdm(range(1,pages+1)):
        #신문사 내 특정 페이지 호출
        page_url = Press_URL+"&page="+str(page)
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
            req = requests.get(link, headers=headers)
            bs = BeautifulSoup(req.text, 'html.parser')

            title = bs.find('h2').get_text()
            #title = bs.select('h2')[0].get_text()
            if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
                continue
            else:
                title_list.append(title)

            #언론명
            if i == '032':
                press = "경향신문"
            elif i == '005' :
                press = "국민일보"
            elif i == '020' :
                press = "동아일보"
            elif i == '021' :
                press = "문화일보"
            elif i == '081' :
                press = "서울신문"
            elif i == '022' :
                press = "세계일보"
            elif i == '023' :
                press = "조선일보"
            elif i == '025' :
                press = "중앙일보"
            elif i == '028' :
                press = "한겨레"
            elif i == '469' :
                press = "한국일보"
            elif i == '009' :
                press = "매일경제"
            elif i == '011' :
                press = "서울경제"
            elif i == '366' :
                press = "조선비즈"
            elif i == '015' :
                press = "한국경제"

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
            print("[", press,"]", title)
            time.sleep(random.random()*4)

        time.sleep(2+random.random()*3)
    print(f"{press} 완료")
    time.sleep(3+random.random()*3)

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
print("news collect complete")