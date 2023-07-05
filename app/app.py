import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import datetime
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


from components.login import render_login
from components.states import init_states
from components.main_page import render_main_page
from components.side_bar import render_side_bar
from utils.filter_dataframe import filter_dataframe
from utils.df_downloader import to_csv
from utils.station_id_dict import station_id_dict

plt.rcParams['font.family'] = 'AppleGothic'


st.set_page_config(
    page_title="BTC_Traffic_Data",
    page_icon='🚆',
    layout='wide',
    initial_sidebar_state='expanded'
)


def init_sessions():
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = datetime.date(2022, 1, 1)
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = datetime.date(2022, 12, 31)
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = datetime.time(7, 0)
    if 'end_time' not in st.session_state:
        st.session_state['end_time'] = datetime.time(20, 0)
    if 'selected_lines' not in st.session_state:
        st.session_state['selected_lines'] = ['전체']
    if 'selected_stations' not in st.session_state:
        st.session_state['selected_stations'] = ['전체']
    if 'on_offs' not in st.session_state:
        st.session_state['on_offs'] = '전체'
    if 'station_dict' not in st.session_state:
        st.session_state['station_dict'] = station_id_dict


init_sessions()


def insert_commas(x, *args):
    '''
    숫자의 천 단위마다 콤마를 찍어주는 formatter
    '''
    return "{:,.0f}".format(x)

# @st.cache_data


def show_data(df):
    st.write('### 📊 데이터')
    st.success(f'✨ {insert_commas(df.shape[0])} 개의 데이터를 찾았습니다.')
    st.dataframe(df.head(150000), use_container_width=True)


# @st.cache_data
def extract_data(df):
    combined_start_datetime = datetime.datetime.combine(
        st.session_state['start_date'], st.session_state['start_time'])
    combined_end_datetime = datetime.datetime.combine(
        st.session_state['end_date'], st.session_state['end_time'])
    extracted_df = df[combined_start_datetime:combined_end_datetime]

    # 호선 필터 적용
    if '전체' in st.session_state['selected_lines']:
        selected_lines = [1, 2, 3, 4]
    else:
        selected_lines = [int(i[0])
                          for i in st.session_state['selected_lines']]
    if 1 in selected_lines:
        selected_lines.append(0)

    df_result = extracted_df.loc[(
        extracted_df['id'] // 100).isin(selected_lines)]

    # 역별 필터 적용
    if '전체' not in st.session_state['selected_stations']:
        selected_stations = [i.split()[0]
                             for i in st.session_state['selected_stations']]
        df_result = df_result.loc[df_result['name'].isin(selected_stations)]

    return df_result


@st.cache_data
def load_data():
    return pd.read_pickle('./data/df_cleaned.pickle')


df = load_data()

# sidebar section
with st.sidebar:
    st.sidebar.title("데이터 필터")
    st.write('수동으로 지정하는 필터와 챗봇을 활용한 자연어 필터를 선택가능합니다.')
    with st.expander('수동 필터', expanded=True):
        st.write('### 1. 날짜 및 시간대 선택')
        col1, _, col2 = st.columns([1, 0.1, 1])

        with col1:
            st.date_input(
                '시작일',
                value=st.session_state["start_date"],
                min_value=df.index.min(),
                max_value=df.index.max(),
                key="start_date"
            )
            st.time_input(
                label='시작시간',
                value=st.session_state["start_time"],
                step=60*60,
                key="start_time")
        with col2:
            st.date_input(
                '종료일',
                value=st.session_state["end_date"],
                min_value=df.index.min(),
                max_value=df.index.max(),
                key="end_date"
            )
            st.time_input(
                label='종료시간',
                value=st.session_state["end_time"],
                step=60*60,
                key="end_time")

        st.markdown('### 2. 호선 및 역 선택')
        # 1호선, 2호선, 3호선, 4호선, 환승역, TOP10, TOP50  등으로 분류를 추가해준다.
        selected_lines = st.multiselect(
            label='호선(전체선택시 하위 필터는 무시)',
            default=['전체'],
            options=['전체', '1호선', '2호선', '3호선', '4호선'],
            help='호선을 선택합니다. 여러 값을 선택할 수 있습니다.',
            key='selected_lines'
        )

        # selected_stations를 동적으로 추출하는 부분
        if '전체' in selected_lines:
            selected_lines_processed = [1, 2, 3, 4]
        else:
            selected_lines_processed = [int(i[0])
                                        for i in st.session_state['selected_lines']]
        if 1 in selected_lines_processed:
            selected_lines_processed.append(0)
        selected_stations_option = []

        for key, val in st.session_state['station_dict'].items():
            if key // 100 in selected_lines_processed:
                selected_stations_option.append(val + ' (' + str(key) + ')')

        selected_stations = st.multiselect(
            label='역명 (전체선택시 하위 필터는 무시)',
            default=['전체'],
            options=['전체'] + selected_stations_option,
            help='역명을 선택합니다. 선택된 호선에 따라 변경됩니다.',
            key='selected_stations'
        )
        st.write('### 3. 승하차 선택')
        selected_onoffs = st.selectbox(
            label='승하차',
            options=['전체', '승차만', '하차만'],
            key='on_offs'
        )

    with st.expander('챗봇 필터'):
        st.write('챗봇 필터')
    st.write('💌 seoldonghun@humetro.busan.kr')

# main section
st.title("BTC_Traffic_Data")
extracted_df = extract_data(df)
if extracted_df.shape[0] == 0:
    st.error('🚨 데이터가 없습니다. 필터를 다시 설정해주세요.')
    st.stop()
col1, _, col2 = st.columns([1, 0.1, 1])
with col1:
    show_data(extracted_df)
    to_csv(extracted_df)
with col2:
    st.write('### 💬 챗봇에게 데이터에 대해 질문하기')

# graph section


def show_graph(df):
    st.write('### 📈 그래프')

    # plt.ticklabel_format(style='plain', axis='x')
    plt.figure(figsize=(10, 10))
    sns.barplot(data=df, y='name',
                x='traffic', estimator='sum', errorbar=None, width=0.5)
    formatter = FuncFormatter(insert_commas)
    plt.gca().xaxis.set_major_formatter(formatter)
    st.pyplot(plt.gcf())
    plt.clf()

    sns.lineplot(data=df.head(100),
                 x=df.head(100).index, y='traffic', hue='name')
    st.pyplot(plt.gcf())


show_graph(extracted_df)

with st.expander('session_states for debugging'):
    st.write(st.session_state)
# 1호선, 2호선, 3호선, 4호선, 환승역, TOP10, TOP50  등으로 분류를 추가해준다.
