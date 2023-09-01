import streamlit as st
from streamlit_option_menu import option_menu

with st.container():
    st.subheader("Today 페이지")
    st.write(" ☞ 12개 조간 신문사(조선, 중앙, 동아, 국민, 서울, 세계, 한국, 경향, 한겨레, 매경, 한경, 서경)의 지면기사를 분석,제공합니다")
    st.write("    매일 아침 7시에 업데이트되며, 일요일 등 조간신문이 발간되지 않는 날에는 전일 분석내용을 제공합니다")