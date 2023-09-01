import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import re

file_path = "/home/ubuntu/test2/full_result.csv"
data = pd.read_csv(file_path)

#################################################################.

data.reset_index(drop=True, inplace=True)
del data['Unnamed: 0']

def same_word(sentence):
    st = sentence
    st = re.sub('기재부', '기획재정부', str(st))
    st = re.sub('과기부', '과학기술정보통신부', str(st))
    st = re.sub('과기정통부', '과학기술정보통신부', str(st))
    st = re.sub('행안부', '행정안전부', str(st))
    st = re.sub('문체부', '문화체육관광부', str(st))
    st = re.sub('농식품부', '농림축산식품부', str(st))
    st = re.sub('산업부', '산업통상자원부', str(st))
    st = re.sub('산자부', '산업통상자원부', str(st))
    st = re.sub('고용부', '고용노동부', str(st))
    st = re.sub('여가부', '여성가족부', str(st))
    st = re.sub('국토부', '국토교통부', str(st))
    st = re.sub('해수부', '해양수산부', str(st))
    st = re.sub('중기부', '중소벤처기업부', str(st))
    st = re.sub('중기벤처부', '중소벤처기업부', str(st))
    st = re.sub('인사처', '인사혁신처', str(st))
    st = re.sub('인혁처', '인사혁신처', str(st))
    st = re.sub('식약처', '식품의약품안전처', str(st))
    st = re.sub('공정위', '공정거래위원회', str(st))
    st = re.sub('개인정보위', '개인정보보호위원회', str(st))
    st = re.sub('개보위', '개인정보보호위원회', str(st))
    st = re.sub('원안위', '원자력안전위원회', str(st))
    st = re.sub('국조실', '국무조정실', str(st))
    st = re.sub('국무총리실', '국무조정실', str(st))
    st = re.sub('대통령실', '대통령비서실', str(st))
    st = re.sub('한 총리', '한덕수', str(st))
    return st



def date_keyword_search(search_word, today): #날짜는 2022-11-10 형식으로 입력
  #키워드 입력
  #대상기간 내 기사 본문 추출
  date_data = data[data['Date']==today]

  #특정 키워드 기사 index 추출(제목에 포함 or 본문에 3번 이상 포함)
  department = []
  press_list = []
  title_link_list = []
  date = []
  sentiment_list = []
  for i in range(0, len(date_data)):
    press = date_data.iloc[i, 0]
    link = date_data.iloc[i, 1]
    title = date_data.iloc[i,2]
    title_re = same_word(title)
    body = date_data.iloc[i,4]
    body_re = same_word(body)
    sentiment = date_data.iloc[i,5]
    if title_re.count(search_word)>0 or body_re.count(search_word) >2:
        title_link = f'''<a href="{link}">{title} ({press})</a>'''
        title_link_list.append(title_link)
        department.append(search_word)
        date.append(today)
        sentiment_list.append(sentiment)
        

  search_result = pd.DataFrame({'title': title_link_list, 'department' : department, 'sentiment' : sentiment_list, 'date' : today})
  search_result.index = search_result.index + 1

  return search_result


now = datetime.now(timezone('Asia/Seoul'))
today = str(now.date())
#today = re.sub('-', '', today)
#today = int(today)
if len(data[data['Date']==today]) != 0:
  president = date_keyword_search("대통령비서실", today)
  prime = date_keyword_search("한덕수", today)
  opm = date_keyword_search("국무조정실", today)
  moef = date_keyword_search("기획재정부", today)
  moe = date_keyword_search("교육부", today)
  msit = date_keyword_search("과학기술정보통신부", today)
  mofa = date_keyword_search("외교부", today)
  unikorea = date_keyword_search("통일부", today)
  moj = date_keyword_search("법무부", today)
  mnd = date_keyword_search("국방부", today)
  mois = date_keyword_search("행정안전부", today)
  mcst = date_keyword_search("문화체육관광부", today)
  mafra = date_keyword_search("농림축산식품부", today)
  motie = date_keyword_search("산업통상자원부", today)
  mohw = date_keyword_search("보건복지부", today)
  me = date_keyword_search("환경부", today)
  moel = date_keyword_search("고용노동부", today)
  mogef = date_keyword_search("여성가족부", today)
  molit = date_keyword_search("국토교통부", today)
  mof = date_keyword_search("해양수산부", today)
  mss = date_keyword_search("중소벤처기업부", today)
  mpva = date_keyword_search("국가보훈부", today)
  ftc = date_keyword_search("공정거래위원회", today)
  fsc = date_keyword_search("금융위원회", today)
  acrc = date_keyword_search("국민권익위원회", today)
  pipc = date_keyword_search("개인정보보호위원회", today)
  nssc = date_keyword_search("원자력안전위원회", today)
  kcc = date_keyword_search("방송통신위원회", today)
  mpm = date_keyword_search("인사혁신처", today)
  moleg = date_keyword_search("법제처", today)
  mfds = date_keyword_search("식품의약품안전처", today)


  result = pd.concat([president, prime, opm, moef, moe, msit, mofa, unikorea, moj, mnd, mois, mcst, mafra, 
  motie, mohw, me, moel, mogef, molit, mof, mss, mpva, ftc, fsc, acrc, pipc, nssc, kcc, mpm, moleg, mfds])

  result.to_csv("/home/ubuntu/test2/today_department_table.csv")

  now = datetime.now(timezone('Asia/Seoul'))
  now = now.strftime('%y-%m-%d %H %M %S')
  print(f"{now} today_make 완료")