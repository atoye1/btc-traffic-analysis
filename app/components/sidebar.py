import streamlit as st
import datetime

from ai.parse_filter import get_json_result


def render_normal_filter(df):
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
            value=datetime.time(7, 0, 0),
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
            value=datetime.time(23, 0, 0),
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
            selected_stations_option.append(
                val + ' (' + str(key) + ')')

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
    pass


def render_ai_filter(df):
    st.text_input('메시지', key='chatbot_filter_input')
    if st.session_state['chatbot_filter_input']:
        parsed_json = get_json_result(
            df, st.session_state['chatbot_filter_input'])
        st.success('✨' + parsed_json['input_summary'])
        st.json(parsed_json)
        st.session_state['chatbot_filter_output'] = parsed_json
        # 인공지능의 아웃풋으로 얻은 json을 세션스테이트에 저장
    else:
        st.session_state['chatbot_filter_output'] = {}
        st.warning('⚠️ 인공지능 필터를 사용하려면 메시지를 입력해주세요.')


def render_sidebar(df):
    with st.sidebar:
        st.sidebar.title("데이터 필터")
        st.write('UI를 활용한 필터와 인공지능을 활용한 필터를 활용가능합니다.')
        st.radio('필터 선택', horizontal=True, options=[
            '일반 필터', '인공지능 필터'], key='filter_selection')
        if st.session_state['filter_selection'] == '일반 필터':
            render_normal_filter(df)

        elif st.session_state['filter_selection'] == '인공지능 필터':
            render_ai_filter(df)

        st.write('💌 seoldonghun@humetro.busan.kr')
        pass