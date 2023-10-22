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


previous_df = pd.read_csv('/home/ubuntu/test2/full_result.csv')
del previous_df["Unnamed: 0"]
full_df = previous_df


ua = UserAgent()

days = ['월', '화', '수', '목', '금', '토', '일']

now = datetime.now(timezone('Asia/Seoul'))
weekday = days[datetime.date(now).weekday()]

date = now.date()
date = str(date)

target_date = re.sub('-', '', date)


press_numbers = ['032', '005', '020', '081', '022', '023', '025', '028', '469', '009', '011', '366', '015']




for i in press_numbers:
    press_list = []
    url_list = []
    title_list = []
    date_list = []
    body_list = []
    weekday_list = []

    #신문사 첫 페이지 정보 읽기
    Press_URL = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid="+str(i)+"&listType=paper&date="+str(target_date)
    headers = {'User-Agent': ua.random}
    req = requests.get(Press_URL, headers=headers)
    bs = BeautifulSoup(req.text, 'html.parser')


    for page in tqdm(range(1,9)): #pages+1
        #신문사 내 특정 페이지 호출
        page_url = Press_URL+"&page="+str(page)
        headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': Press_URL,
        'Accept-Encoding': 'gzip, deflate, br', 
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
        }
        req = requests.get(page_url, headers=headers)
        bs = BeautifulSoup(req.text, 'html.parser')

        if bs is None:
            now = datetime.now(timezone('Asia/Seoul'))
            now = now.strftime('%y-%m-%d %H %M %S')
            print(f"{now} 연결 끊김. 1차 재시도 예정..")
            time.sleep(200)
            headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': Press_URL,
            'Accept-Encoding': 'gzip, deflate, br', 
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
            }
            req = requests.get(page_url, headers=headers)
            bs = BeautifulSoup(req.text, 'html.parser')

            allbreak = False
            press = "경향신문" if i =='032' else "국민일보" if i=="005" else "동아일보" if i=="020" else "서울신문" if i=="081" else "세계일보" if i=="022" else "조선일보" if i=="023" else "중앙일보" if i=="025" else "한겨레" if i=="028" else "한국일보" if i=="469"else "매일경제" if i=="009" else "서울경제" if i=="011" else "조선비즈" if i=="366" else "한국경제"
            #특정 페이지 내 기사목록 추출
            if len(bs.select('ul.type13')) != 0:
                ul_tags = bs.select('ul.type13')
                for ul_tag in ul_tags:
                    li_tags = ul_tag.select('li')
                    for li_tag in li_tags:
                        link = li_tag.a['href']
                        title = li_tag.a.get_text()
                        if title == "" :
                            if li_tag.img is None:  
                                pass
                            else:
                                title = li_tag.img['alt']
                        if link in url_list:
                            allbreak = True
                            break
                        else:
                            if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
                                pass
                            else:
                                url_list.append(link)
                                title_list.append(title)
                                press_list.append(press)
                                date_list.append(date)
                                body_list.append("")
                                weekday_list.append(weekday)

                    if allbreak == True:
                        break
                if allbreak == True:
                    continue

            ul_tags = bs.select('ul.type02')
            for ul_tag in ul_tags:
                li_tags = ul_tag.select('li')
                for li_tag in li_tags:
                    link = li_tag.a['href']
                    title = li_tag.a.get_text()
                    if title == "" :
                        if li_tag.img is None:  
                            pass
                        else:
                            title = li_tag.img['alt']
                    if link in url_list:
                        allbreak = True
                        break    
                    else:
                        if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
                            pass
                        else:
                            url_list.append(link)
                            title_list.append(title)
                            press_list.append(press)
                            date_list.append(date)
                            body_list.append("")
                            weekday_list.append(weekday)
                if allbreak == True:
                    break
            if allbreak == True:
                continue

        else:
            allbreak = False
            press = "경향신문" if i =='032' else "국민일보" if i=="005" else "동아일보" if i=="020" else "서울신문" if i=="081" else "세계일보" if i=="022" else "조선일보" if i=="023" else "중앙일보" if i=="025" else "한겨레" if i=="028" else "한국일보" if i=="469"else "매일경제" if i=="009" else "서울경제" if i=="011" else "조선비즈" if i=="366" else "한국경제"
            #특정 페이지 내 기사목록 추출
            if len(bs.select('ul.type13')) != 0:
                ul_tags = bs.select('ul.type13')
                for ul_tag in ul_tags:
                    li_tags = ul_tag.select('li')
                    for li_tag in li_tags:
                        link = li_tag.a['href']
                        title = li_tag.a.get_text()
                        if title == "" :
                            if li_tag.img is None:  
                                pass
                            else:
                                title = li_tag.img['alt']
                        if link in url_list:
                            allbreak = True
                            break
                        else:
                            if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
                                pass
                            else:
                                url_list.append(link)
                                title_list.append(title)
                                press_list.append(press)
                                date_list.append(date)
                                body_list.append("")
                                weekday_list.append(weekday)

                    if allbreak == True:
                        break
                if allbreak == True:
                    continue

            ul_tags = bs.select('ul.type02')
            for ul_tag in ul_tags:
                li_tags = ul_tag.select('li')
                for li_tag in li_tags:
                    link = li_tag.a['href']
                    title = li_tag.a.get_text()
                    if title == "" :
                        if li_tag.img is None:  
                            pass
                        else:
                            title = li_tag.img['alt']
                    if link in url_list:
                        allbreak = True
                        break    
                    else:
                        if "[포토]" in title or "[포토뉴스]" in title or "[부고]" in title:
                            pass
                        else:
                            url_list.append(link)
                            title_list.append(title)
                            press_list.append(press)
                            date_list.append(date)
                            body_list.append("")
                            weekday_list.append(weekday)
                if allbreak == True:
                    break
            if allbreak == True:
                continue

        time.sleep(+random.random()*5)
    press = "경향신문" if i =='032' else "국민일보" if i=="005" else "동아일보" if i=="020" else "서울신문" if i=="081" else "세계일보" if i=="022" else "조선일보" if i=="023" else "중앙일보" if i=="025" else "한겨레" if i=="028" else "한국일보" if i=="469"else "매일경제" if i=="009" else "서울경제" if i=="011" else "조선비즈" if i=="366" else "한국경제"

    result = {'Press' : press_list, 'Url' : url_list, 'Title':title_list, 'Date':date_list, 'Body':body_list, 'Weekday':weekday_list}
    df=pd.DataFrame(result)
    df = df.drop_duplicates(['Title'], keep='first')
    df.reset_index(drop=True, inplace=True)
    df['Sentiment'] = ''
    
    full_df = pd.concat([full_df, df])
    full_df.to_csv('/home/ubuntu/test2/full_result.csv')
    
    now = datetime.now(timezone('Asia/Seoul'))
    now = now.strftime('%y-%m-%d %H %M %S')
    print(f"{now} {press} 완료")
    time.sleep(2+random.random()*8)

full_df = full_df.drop_duplicates(['Url'], keep='first')
full_df.reset_index(drop=True, inplace=True)
full_df.to_csv('/home/ubuntu/test2/full_result.csv')
now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} news collect complete")