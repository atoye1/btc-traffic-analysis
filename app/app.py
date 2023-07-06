import streamlit as st
import pandas as pd

from components.data_tab import render_data_tab
from components.analysis_tab import render_analysis_tab
from components.graph_tab import render_graph_tab
from components.sidebar import render_sidebar
from components.init_session_states import init_session_states

from utils.load_raw_data import load_raw_data
from utils.filter_dataframe import filter_dataframe

st.set_page_config(
    page_title="BTC_Traffic_Data",
    page_icon='🚆',
    layout='wide',
    initial_sidebar_state='expanded'
)

init_session_states()

df_raw = load_raw_data()

# sidebar section
render_sidebar(df_raw)

# main section
st.title("부산교통공사 시간대별 승하차 데이터")
st.write("아래의 탭에서 원하는 기능을 선택하세요")

df_filtered = filter_dataframe(df_raw)
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["데이터", "분석", "그래프", "AI에게 질문하기", "전체 데이터 분석"])
with tab1:
    render_data_tab(df_filtered)
with tab2:
    render_analysis_tab(df_filtered)
with tab3:
    render_graph_tab(df_filtered)
with tab4:
    st.write('AI에게 질문하는 컴포넌트가 들어갈 예정입니다.')
with tab5:
    st.write('필터가 적용되지 않은 전체 데이터를 기반으로 분석한 결과 리포트')

with st.expander('session_states for debugging'):
    st.write(st.session_state)
