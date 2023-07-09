import streamlit as st
from utils.formatters import insert_commas


@st.cache_data(show_spinner='데이터를 화면에 표시하는 중입니다.')
def render_dataframe(df):
    st.dataframe(df.head(150000), use_container_width=True, height=700)
