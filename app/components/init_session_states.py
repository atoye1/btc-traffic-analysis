import streamlit as st

from utils.station_id_dict import station_id_dict
from utils.constants import *


def init_session_states():
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = DEFAULT_START_DATE
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = DEFAULT_START_TIME
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = DEFAULT_END_DATE
    if 'end_time' not in st.session_state:
        st.session_state['end_time'] = DEFAULT_END_TIME
    if 'selected_lines' not in st.session_state:
        st.session_state['selected_lines'] = DEFAULT_SELECTED_LINES
    if 'selected_stations' not in st.session_state:
        st.session_state['selected_stations'] = DEFAULT_SELECTED_STATIONS
    if 'on_off' not in st.session_state:
        st.session_state['on_off'] = DEFAULT_ON_OFF
    if 'filter_selection' not in st.session_state:
        st.session_state['filter_selection'] = DEFAULT_FILTER_SELECTION
    if 'chatbot_filter_input' not in st.session_state:
        st.session_state['chatbot_filter_input'] = DEFAULT_CHATBOT_FILTER_INPUT
    if 'chatbot_filter_output' not in st.session_state:
        st.session_state['chatbot_filter_output'] = DEFAULT_CHATBOT_FILTER_OUTPUT
    if 'station_dict' not in st.session_state:
        st.session_state['station_dict'] = station_id_dict
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [
            '안녕하세요, 필터링된 데이터에 관해 궁금한 내용을 입력해주세요.']
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = []
    if 'cost' not in st.session_state:
        st.session_state['cost'] = []
    if 'total_tokens' not in st.session_state:
        st.session_state['total_tokens'] = []
    if 'total_cost' not in st.session_state:
        st.session_state['total_cost'] = 0.0
