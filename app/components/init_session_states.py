import streamlit as st
import datetime

from utils.station_id_dict import station_id_dict


def init_session_states():
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = datetime.date(2014, 1, 1)
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = datetime.date(2023, 1, 1)
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = datetime.time(7, 0, 0)
    if 'end_time' not in st.session_state:
        st.session_state['end_time'] = datetime.time(23, 0, 0)
    if 'selected_lines' not in st.session_state:
        st.session_state['selected_lines'] = ['전체']
    if 'selected_stations' not in st.session_state:
        st.session_state['selected_stations'] = ['전체']
    if 'on_offs' not in st.session_state:
        st.session_state['on_offs'] = '전체'
    if 'filter_selection' not in st.session_state:
        st.session_state['filter_selection'] = '일반 필터'
    if 'station_dict' not in st.session_state:
        st.session_state['station_dict'] = station_id_dict
    if 'chatbot_filter_input' not in st.session_state:
        st.session_state['chatbot_filter_input'] = ''
