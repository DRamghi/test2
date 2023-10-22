import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import re
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Mecab
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import stylecloud


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
month_ago = now-timedelta(days=30)
month_ago = str(month_ago.date())
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

##############################################


  #최근 1달간 DB 추출
  sub_data = data[data['Date'].between(month_ago, today)]

  date_range = list(set(sub_data['Date']))
  date_range.sort()

  ##날짜별 키워드 빈도수 데이터프레임

  add_stop_words = '이번 담당 인터뷰 여러분 관련 이날 이후 오후 지음 보도 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간 우리 행위 부문 외부 내년 사실 내용 현지 계기 구성 당시 오늘 그날 참석 시일 의견 수렴 검토 요청 이유 논의 과정 의미 확정 사업 사건 주변 사람 상태 누군가 정도 이곳 일대 당시 동안 마련 근처 정도 느낌 소식 그곳 이곳 이상 이번 담당 여러분 관련 이날 이후 오후 지음 오전 경우 기간 때문 관계자 최근 기준 설명 연합뉴스 예정 증가 가운데 상당 가량 추진 아마 대략 방침 현지시간'
  add_stop_words = add_stop_words.split(' ')
  #add_stop_words.extend(list(stop_words))

  keywords = pd.Series()
  tagger = Mecab()
  for i in date_range:
    word_list = []
    date_body = data[data['Date'] == i]  #특정날짜에 해당하는 데이터프레임 추출

    #기사마다 최초 100단어만 추출
    date_body_list = []
    for j in range(0, len(date_body)):
      if len(date_body.iloc[j,4]) > 100:
        date_body_list.append(date_body.iloc[j,4][0:100])  #본문
        date_body_list.append(date_body.iloc[j,2])  #제목은 2번 추출(가중치)
        date_body_list.append(date_body.iloc[j,2])


    #date_body = date_body['Body'].tolist() # 해당 기사본문을 리스트화

    date_body = ' '.join(date_body_list)
    date_words = tagger.nouns(date_body)


    ##bigram도 추가
    for j in range(len(date_words)-2):
      date_words.append(f"{date_words[j]} {date_words[j+1]} {date_words[j+2]}")
      date_words.append(f"{date_words[j]} {date_words[j+1]}")
    date_words.append(f"{date_words[j+1]} {date_words[j+2]}")

    for word in date_words:
      if len(word)>1 and word not in add_stop_words:
        word_list.append(word)
    noun_count = Counter(word_list)
    noun_count = pd.Series(noun_count)
    noun_count.name = i
    keywords = pd.concat([keywords,noun_count], axis=1)
  keywords = keywords.drop(0, axis=1)

  keywords = keywords.fillna(0)  #NaN은 0으로 변경(평균 처리 위해)

  #빈도수가 급증한 키워드 추출

  if len(data[data['Date']==today]) > 800 :
    a = keywords[((keywords.iloc[:,-1]>25)) & ((keywords.iloc[:,-1]>keywords.mean(axis='columns')*1.5))]   # & (keywords.iloc[:,-1]) > keywords.iloc[:,-2]
  elif len(data[data['Date']==today]) > 700 :
    a = keywords[((keywords.iloc[:,-1]>20)) & ((keywords.iloc[:,-1]>keywords.mean(axis='columns')*1.5))]   # & (keywords.iloc[:,-1]) > keywords.iloc[:,-2]
  else:
    a = keywords[((keywords.iloc[:,-1]>15)) & ((keywords.iloc[:,-1]>keywords.mean(axis='columns')*1.5))]   # & (keywords.iloc[:,-1]) > keywords.iloc[:,-2]
  b = a.sort_values(by=[keywords.columns[-1]],ascending=False)

  #"일 "로 시작되는 n-gram 삭제
  short_list = []
  for i in range(0,len(b)): 
    if b.index[i][0:2] == "일 ":
        short_list.append(b.index[i])
    elif b.index[i][0:2] == "월 ":
        short_list.append(b.index[i])
    elif b.index[i][-2:] == " 년":
        short_list.append(b.index[i])
  c = b.drop(short_list, axis = 0)
    

  #2개 단어가 있는 경우 1개 단어는 삭제
  short_list = []
  for i in range(0,len(c)): 
    similar_count = 0
    similar_index_list = []
    for j in range(0,len(c)): 
      if j == i:
        pass

      elif c.index[i] in c.index[j] : #and b.iloc[:,-1][i]/2 < b.iloc[:,-1][j]:
        #b.loc[j,-1] = b.loc[j,-1] + b.loc[i,-1]/2
        short_list.append(c.index[i])
        similar_count = similar_count + 1
        similar_index_list.append(j)
    for similar_index in similar_index_list:
      c.iloc[similar_index,-1] = c.iloc[similar_index,-1] + c.iloc[i,-1]/similar_count
  c = c.drop(short_list, axis = 0)
  #top_related_words = c.iloc[:,-1][0:50].to_dict()
  today_issue = c.iloc[:,-1]

  # n-gram 편집
  overlap_list = []

  subword_list = []
  for i in c.index :
    subword = i.split(' ')
    if len(subword) > 1: #n-gram 추출
      if len(subword) == 2 and len(i) <=3 :  # 1글자로만 된 n-gram 삭제
        overlap_list.append(i)
      elif len(subword) == 3 and len(i) <= 6 :
        overlap_list.append(i)
      elif len(subword) == 3 and len(i) > 9 :
        overlap_list.append(i)
      else:
        subword_list.append(subword)

  #subword 중 글자가 70% 이상 같은것은 작은단어 삭제
  for i in subword_list:
    for j in subword_list:
      if i == j:
        pass
      else:
        same = [x for x, y in zip(i,j) if x == y]  #두 리스트 비교, 같은 값 개수 확인
        if len(same)/(len(' '.join(i))+len(' '.join(j))) > 0.7 :
          if len(i) > len(j):
              overlap_list.append(' '.join(j))
              today_issue.loc[' '.join(i)] = today_issue.loc[' '.join(i)] + today_issue.loc[' '.join(j)]


  today_issue.drop(overlap_list, axis=0, inplace=True)

  top_related_words = today_issue[0:50].to_dict()
  print(top_related_words)

  stopwords = "국가 현장 참여 계획 결정 회의 조성 사회"
  stopwords = stopwords.split(' ')


  stylecloud.gen_stylecloud(text = top_related_words,
                          #palette="cartocolors.diverging.TealRose_7", #"colorbrewer.diverging.Spectral_11",
                          background_color='white',
                          #gradient="horizontal",
                          output_name="/home/ubuntu/test2/wordcloud.png",
                          font_path='NanumGothic.ttf',
                          custom_stopwords=stopwords)  

  # wc = WordCloud(background_color='white', font_path='NanumGothic.ttf')
  # wc.generate_from_frequencies(top_related_words)
  # figure = plt.figure()
  # plt.imshow(wc, interpolation='bilinear')
  # plt.axis('off')
  # plt.show()
  # plt.savefig('wordcloud.png', bbox_inches='tight', pad_inches=0)
  # plt.close(figure)




now = datetime.now(timezone('Asia/Seoul'))
now = now.strftime('%y-%m-%d %H %M %S')
print(f"{now} today_make 완료")

