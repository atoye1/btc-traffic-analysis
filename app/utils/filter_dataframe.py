import datetime
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner='데이터를 필터링 중입니다.')
def filter_dataframe(df):
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
        start_date = datetime.date(
            chatbot_filter_output['start_date']) if chatbot_filter_output['start_date'] else st.session_state['start_date']
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
