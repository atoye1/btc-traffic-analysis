import datetime
import pandas as pd
import streamlit as st
from utils.constants import *
from data.line_stations import line_stations

# TODO 어플리케이션의 안정적인 확장을 위해 테스트 코드 및 테스트 케이스 작성 필요
# TODO 객체지향 형식으로 필터클래스를 정의해야함.
# TODO pydantic 등으로 입력값 검증하는 로직도 필요함.


@st.cache_data(show_spinner='데이터를 필터링 중입니다.')
def filter_dataframe(df=None,
                     filter_selection=DEFAULT_FILTER_SELECTION,
                     start_date=DEFAULT_START_DATE,
                     start_time=DEFAULT_START_TIME,
                     end_date=DEFAULT_END_DATE,
                     end_time=DEFAULT_END_TIME,
                     selected_lines=DEFAULT_SELECTED_LINES,
                     selected_stations=DEFAULT_SELECTED_STATIONS,
                     on_off=DEFAULT_ON_OFF,
                     chatbot_filter_output=DEFAULT_CHATBOT_FILTER_OUTPUT,
                     ):
    if df is None:
        return pd.DataFrame()

    if filter_selection == '인공지능 필터':
        if not chatbot_filter_output:
            return pd.DataFrame()

        # 인공지능 필터인 경우 필터링 변수를 chatbot_filter_output에서 가져옴
        start_date = datetime.datetime.strptime(
            chatbot_filter_output['start_date'], '%Y-%m-%d')
        start_date = start_date.date()
        end_date = datetime.datetime.strptime(
            chatbot_filter_output['end_date'], '%Y-%m-%d')
        end_date = end_date.date()
        start_time = datetime.time(int(chatbot_filter_output['start_time']))
        end_time = datetime.time(int(chatbot_filter_output['end_time']))
        selected_lines = chatbot_filter_output['selected_lines']
        selected_stations = chatbot_filter_output['selected_stations']
        on_off = chatbot_filter_output['on_off']

    # UI 필터인 경우 변수를 정리해줘야 한다.
    selected_stations = [i.split()[0] for i in selected_stations]

    combined_start_datetime = datetime.datetime.combine(
        start_date, start_time)
    combined_end_datetime = datetime.datetime.combine(
        end_date, end_time)
    datetime_filtered_df = df[combined_start_datetime:
                              combined_end_datetime]
    assert datetime_filtered_df.shape[0] > 0, '조건에 맞는 데이터가 없습니다.'
    # datetime_filtered_df = df[start_date:end_date + datetime.timedelta(days=1)]
    # datetime_filtered_df = datetime_filtered_df[(datetime_filtered_df.index.time >= start_time) & (
    #     datetime_filtered_df.index.time <= end_time)]

    if on_off == '승차':
        datetime_filtered_df = datetime_filtered_df[datetime_filtered_df['on']]
    elif on_off == '하차':
        datetime_filtered_df = datetime_filtered_df[~datetime_filtered_df['on']]

    if '전체' in selected_lines:
        selected_lines = ['1호선', '2호선', '3호선', '4호선']
    if '전체' in selected_stations or filter_selection == '인공지능 필터':
        for line in selected_lines:
            selected_stations += line_stations[line]
    selected_stations = list(set(selected_stations))
    df_result = datetime_filtered_df.loc[datetime_filtered_df['name'].isin(
        selected_stations)]
    return df_result
