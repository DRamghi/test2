import streamlit as st
from streamlit_option_menu import option_menu

with st.container():
    st.subheader("실시간 뉴스 키워드 알람 서비스 제공")
    st.write("원하는 키워드에 대한 인터넷 뉴스기사 발생시, 1시간 이내 텔레그램으로 알림메시지를 발송하는 서비스를 제공합니다.")
    st.write("(매 정각마다 키워드에 대한 뉴스기사 검색, 1시간 이내 업로드된 기사가 있는 경우 알림메시지 발신)")
with st.container():
    st.subheader("서비스 이용방법")