import streamlit as st
from utils.formatters import insert_commas


@st.cache_data(show_spinner='데이터를 화면에 표시하는 중입니다.')
def render_dataframe(df):
    st.write('### 📊 데이터')
    st.success(f'✨ {insert_commas(df.shape[0])} 개의 데이터를 찾았습니다.')
    st.dataframe(df.head(150000), use_container_width=True)
