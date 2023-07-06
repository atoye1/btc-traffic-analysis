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
from components.init_session_states import init_session_states
from utils.filter_dataframe import filter_dataframe
from utils.df_downloader import to_csv
from ai.parse_filter import get_json_result

plt.rcParams['font.family'] = 'AppleGothic'


st.set_page_config(
    page_title="BTC_Traffic_Data",
    page_icon='🚆',
    layout='wide',
    initial_sidebar_state='expanded'
)

init_session_states()


def insert_commas(x, *args):
    '''
    숫자의 천 단위마다 콤마를 찍어주는 formatter
    '''
    return "{:,.0f}".format(x)

# @st.cache_data
def render_data(df):
    st.write('### 📊 데이터')
    st.success(f'✨ {insert_commas(df.shape[0])} 개의 데이터를 찾았습니다.')
    st.dataframe(df.head(150000), use_container_width=True)


def render_graph(df):
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


# @st.cache_data
def extract_data(df):
    if st.session_state['filter_selection'] == '일반 필터':
        print('일반필터 selected')
        combined_start_datetime = datetime.datetime.combine(
            st.session_state['start_date'], st.session_state['start_time'])
        combined_end_datetime = datetime.datetime.combine(
            st.session_state['end_date'], st.session_state['end_time'])
        selected_lines = st.session_state['selected_lines']
        selected_stations = st.session_state['selected_stations']

    elif st.session_state['filter_selection'] == '인공지능 필터':
        print('인공지능 필터 selected')
        chatbot_filter_output = st.session_state['chatbot_filter_output']

        # chatbot_filter_output가 없다면 빈 데이터프레임을 리턴
        if not chatbot_filter_output:
            return pd.DataFrame()
        print(chatbot_filter_output)
        # 값이 없을 때 기본값 설정하기
        # 값이 있을 때 combine 하기
        # 여기까지
        start_date = datetime.date(chatbot_filter_output['start_date']) if chatbot_filter_output['start_date'] else st.session_state['start_date']
        print(start_date)
        
        combined_start_datetime = datetime.datetime.combine(
            chatbot_filter_output['start_date'], chatbot_filter_output['start_time'])
        combined_end_datetime = datetime.datetime.combine(
            chatbot_filter_output['end_date'], chatbot_filter_output['end_time'])
        
        if chatbot_filter_output['selected_lines']:
            selected_lines = chatbot_filter_output['selected_lines']
        if chatbot_filter_output['selected_stations']:
            selected_stations = chatbot_filter_output['selected_stations']
        
    extracted_df = df[combined_start_datetime:combined_end_datetime]
    if '전체' in selected_lines:
        selected_lines = [1, 2, 3, 4]
    else:
        selected_lines = [int(i[0])
                        for i in st.session_state['selected_lines']]
    if 1 in selected_lines:
        selected_lines.append(0)

    # 호선 필터 적용

    df_result = extracted_df.loc[(
        extracted_df['id'] // 100).isin(selected_lines)]
    # 역별 필터 적용
    if '전체' not in selected_stations:
        selected_stations = [i.split()[0]
                             for i in selected_stations]
        df_result = df_result.loc[df_result['name'].isin(selected_stations)]

    return df_result


@st.cache_data
def load_data():
    return pd.read_pickle('./data/df_cleaned.pickle')


df = load_data()

# sidebar section
with st.sidebar:
    st.sidebar.title("데이터 필터")
    st.write('UI를 활용한 필터와 인공지능을 활용한 필터를 활용가능합니다.')
    st.radio('필터 선택', horizontal=True, options=['일반 필터', '인공지능 필터'], key='filter_selection')
    if st.session_state['filter_selection'] == '일반 필터':
        st.write('### 1. 날짜 및 시간대 선택')
        col1, _, col2 = st.columns([1, 0.1, 1])

        with col1:
            st.date_input(
                label='시작일',
                value=datetime.date(2017, 4, 20),
                min_value=df.index.min(),
                max_value=df.index.max(),
                key="start_date"
            )
            st.time_input(
                label='시작시간',
                value=datetime.time(7,0,0),
                step=60*60,
                key="start_time")
        with col2:
            st.date_input(
                label='종료일',
                value=datetime.date(2021, 1, 1),
                min_value=df.index.min(),
                max_value=df.index.max(),
                key="end_date"
            )
            st.time_input(
                label='종료시간',
                value=datetime.time(23,0,0),
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
            selected_lines = [1, 2, 3, 4]
        else:
            selected_lines = [int(i[0])
                                        for i in st.session_state['selected_lines']]
        if 1 in selected_lines:
            selected_lines.append(0)
        selected_stations_option = []

        for key, val in st.session_state['station_dict'].items():
            if key // 100 in selected_lines:
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
    elif st.session_state['filter_selection'] == '인공지능 필터':
        st.text_input('메시지', key='chatbot_filter_input')
        if st.session_state['chatbot_filter_input']:
            parsed_json = get_json_result(df, st.session_state['chatbot_filter_input'])
            st.success('✨' + parsed_json['input_summary'])
            st.json(parsed_json)
            st.session_state['chatbot_filter_output'] = parsed_json
            # 인공지능의 아웃풋으로 얻은 json을 세션스테이트에 저장
        else:
            st.session_state['chatbot_filter_output'] = {}
            st.warning('⚠️ 인공지능 필터를 사용하려면 메시지를 입력해주세요.')
                    
    st.write('💌 seoldonghun@humetro.busan.kr')

# main section
extracted_df = extract_data(df)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚆 데이터", "분석","그래프", "🤖 AI에게 질문하기", "전체 데이터 분석"])
with tab1:
    st.title("BTC_Traffic_Data")
    if extracted_df.shape[0] == 0:
        st.error('🚨 데이터가 없습니다. 필터를 다시 설정해주세요.')
        st.write(st.session_state)
        st.stop()
    with st.spinner('데이터를 불러오는 중입니다...'):
        render_data(extracted_df)
    to_csv(extracted_df)

# graph section
with tab2:
    # st.plotly_chart(px.line(extracted_df, x=extracted_df.index, y='traffic', color='name', title='승하차량 추이'))
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

with tab3:
    with st.spinner('그래프를 그리는 중입니다...'):
        # render_graph(extracted_df)
        pass

with tab4:
    with st.expander('도움말'):
        st.write('실험적인 단계입니다.')

with tab5:
    st.write('# 필터가 적용되지 않은 전체 데이터를 기반으로 분석한 결과')

with st.expander('session_states for debugging'):
    st.write(st.session_state)
# 1호선, 2호선, 3호선, 4호선, 환승역, TOP10, TOP50  등으로 분류를 추가해준다.
