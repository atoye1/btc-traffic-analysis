import streamlit as st
import pandas as pd


@st.cache_data(show_spinner='원본 데이터를 불러오는 중입니다.')
def load_raw_data():
    return pd.read_pickle('./data/df_cleaned.pickle')
