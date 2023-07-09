import streamlit as st
from utils.df_downloader import to_csv
from utils.render_dataframe import render_dataframe
from utils.formatters import insert_commas


def render_data_tab(df):
    st.write('### 📊 데이터')
    if df.shape[0] == 0:
        st.error('🚨 데이터가 없습니다. 필터를 다시 설정해주세요.')
        st.write(st.session_state)
        st.stop()
    st.success(f'✨ {insert_commas(df.shape[0])} 개의 데이터를 찾았습니다.')
    render_dataframe(df)
    print('render_dataframe done')
    to_csv(df)
    print('to_csv done')
