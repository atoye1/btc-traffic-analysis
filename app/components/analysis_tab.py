import streamlit as st


def render_analysis_tab(df):
    st.write('## 분석 (필터링된 데이터 기준으로...)')
    st.write('### 승차 통계')
    st.write('현재 데이터 기준 TOP 10 시간대와 역')
    st.write('현재 데이터 기준 TOP 10 요일과 역')
    st.write('현재 데이터 기준 TOP 10 요일과 시간대')
    st.write('현재 데이터 기준 TOP 10')
    st.write('### 하차 통계')
    st.write('현재 데이터 기준 TOP 10 시간대와 역')
    st.write('현재 데이터 기준 TOP 10 요일과 역')
    st.write('현재 데이터 기준 TOP 10 요일과 시간대')
    st.write('현재 데이터 기준 TOP 10')
    st.write('### 요일별 통계')
    st.write('현재 데이터 기준 TOP 10 시간대와 역')
    st.write('현재 데이터 기준 TOP 10 요일과 역')
    st.write('현재 데이터 기준 TOP 10 요일과 시간대')
    st.write('현재 데이터 기준 TOP 10')
    st.write('### 시간대별 통계')
    st.write('현재 데이터 기준 TOP 10 시간대와 역')
    st.write('현재 데이터 기준 TOP 10 요일과 역')
    st.write('현재 데이터 기준 TOP 10 요일과 시간대')
    st.write('현재 데이터 기준 TOP 10')
    pass
