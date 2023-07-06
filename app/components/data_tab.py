import streamlit as st
from utils.df_downloader import to_csv
from utils.render_dataframe import render_dataframe


def render_data_tab(df):
    if df.shape[0] == 0:
        st.error('🚨 데이터가 없습니다. 필터를 다시 설정해주세요.')
        st.write(st.session_state)
        st.stop()
    render_dataframe(df)
    print('render_dataframe done')
    to_csv(df)
    print('to_csv done')
