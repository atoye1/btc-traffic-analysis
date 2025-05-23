import os
import warnings

import streamlit as st
from components.analysis_tab import render_analysis_tab
from components.chat_tab import render_chat_tab
from components.data_tab import render_data_tab
from components.graph_tab import render_graph_tab
from components.init_session_states import init_session_states
from components.sidebar import render_sidebar
from dotenv import find_dotenv, load_dotenv
from utils.filter_dataframe import filter_dataframe
from utils.load_raw_data import load_raw_data

load_dotenv(find_dotenv())

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="BTC_Traffic_Data",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_states()


# sidebar section
df_raw = load_raw_data()
render_sidebar(df_raw)

# main section
st.title(
    "부산교통공사 시간대별 승하차 데이터",
    help="출처 : https://www.data.go.kr/data/3057229/fileData.do",
)
st.markdown("부산교통공사에서 제공하는 시간대별 승하차 데이터를 조회, 분석합니다.")
st.markdown("인공지능을 활용한 자연어 질의도 가능합니다.")
st.write("### 사용법")
st.write(
    "1. 왼쪽의 사이드바에서 조회하고 싶은 데이터의 기간과 호선, 역, 승하차를 선택합니다."
)
st.write(
    "2. 또는 인공지능 필터를 선택하고, 자연어로 조회하고 싶은 데이터를 입력합니다."
)
st.write("3. 필터링된 데이터를 확인하고, 아래의 탭을 탐색해보세요")

df_raw = load_raw_data()
# st.cache_data 를 적용하기 위해 세션에 저장된 값을 각각 전달.
df_filtered = filter_dataframe(
    df=df_raw,
    filter_selection=st.session_state["filter_selection"],
    start_date=st.session_state["start_date"],
    start_time=st.session_state["start_time"],
    end_date=st.session_state["end_date"],
    end_time=st.session_state["end_time"],
    selected_lines=st.session_state["selected_lines"],
    selected_stations=st.session_state["selected_stations"],
    on_off=st.session_state["on_off"],
    chatbot_filter_output=st.session_state["chatbot_filter_output"],
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["데이터", "AI에게 질문하기", "그래프", "분석", "전체 데이터 분석"]
)
with tab1:
    col1, _, col2 = st.columns([1.5, 0.1, 1])
    with col2:
        render_chat_tab(df_filtered)
    with col1:
        render_data_tab(df_filtered)
with tab2:
    st.write("AI에게 질문하는 컴포넌트가 들어갈 예정입니다.")
with tab3:
    render_graph_tab(df_filtered)
with tab4:
    render_analysis_tab(df_filtered)
with tab5:
    st.write("필터가 적용되지 않은 전체 데이터를 기반으로 분석한 결과 리포트")

with st.expander("session_states for debugging"):
    st.write(st.session_state)
