import os

import pandas as pd
import streamlit as st

from data.ingest_csv_files import ingest_csv_files


@st.cache_data(show_spinner="원본 데이터를 불러오는 중입니다.")
def load_raw_data():
    # search for *.pkl file in ./data dir
    # if there is no file, then read csv files and save it as pickle file
    filepath = "./data/df_cleaned.pkl"
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        ingest_csv_files()

    result = pd.read_pickle("./data/df_cleaned.pkl")
    print("원본 데이터를 불러왔습니다.")
    return result


def load_raw_metadata():
    pass
