import streamlit as st
from streamlit_option_menu import option_menu

with st.container():
    st.subheader("서비스 소개")
    st.write("원하는 키워드에 대한 인터넷 뉴스가 나올 경우 1시간 이내에 텔레그램으로 해당 뉴스 url 발송(키워드당 최대 10건)")
    st.write("(매 정각마다 키워드에 대한 뉴스기사 검색, 1시간 이내 업로드된 기사가 있는 경우 알림메시지 발신)")
    st.write("(0시부터 5시까지는 메시지를 보내지 않고, 아침 6시에 6시간 동안 검색된 뉴스 url을 일괄 발신)")
    st.markdown("""---""")

with st.container():
    st.subheader("서비스 이용방법")
    st.write("스마트폰에서 텔레그램 앱 접속 > 화면 우측상단의 돋보기 클릭 > @drmgg_bot 친구추가(News_BOT으로 나올 수 있음) > 친구목록에서 News_BOT 누르기 > 키워드 입력")
    st.markdown("""---""")

with st.container():
    st.subheader("키워드 입력방법")
    st.write("키워드 추가 : 대화창에 원하는 키워드 입력(별도 반응 없음)")
    st.write("키워드 삭제 : ""ㅇㅇㅇ 삭제"" 입력(키워드와 삭제 간 띄어쓰기가 되어야 인식가능)")
    st.write("키워드는 꼭 한 단어일 필요 없으며, 평소 인터넷에 검색하는 대로 입력 가능(예 : 장관 임명, 국회 예산 본회의 등)")
    st.write('키워드 문구가 반드시 그대로 포함되어야 하는 경우, "  " 활용(예 : "탄소중립")')
    st.markdown("""---""")

with st.container():
    st.subheader("활용 팁")
    st.write("권장 키워드 : 자주 보도되지는 않아서 매번 검색,확인하기는 번거로우나, 뉴스 발생시 꼭 알았으면 하는 키워드(예 : 지진, 개각, 규제개혁위원회 등)")
    st.write("부적절 키워드 : 언론에 수시로 언급되어 알림서비스가 필요없는 키워드(예 : 경제, 정부, 미국 등)")
    

    