import streamlit as st
import datetime

from ai.generate_data_filter import generate_data_filter


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
        # TODO 여기도 역별 메타데이터 테이블을 따로 관리해서, 거기서 정보를 추출한다. 주소, 호선, 환승역, 근무인원, 관리역 여부 등을 관리하는 테이블을 만든다.
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
        options=['전체', '승차', '하차'],
        key='on_off'
    )
    pass


def render_ai_filter(df):
    with st.expander('인공지능 필터 사용법이 궁금하면 클릭하세요'):
        st.markdown("### 소개")
        st.markdown("인공지능 모델을 통해 자연어로 데이터를 필터링할 수 있습니다.")
        st.markdown("모델은 입력받은 자연어를 json형식으로 파싱하고, 앱에 전달합니다.")
        st.markdown("앱은 이를 기반으로 데이터를 필터링해서 보여줍니다.")

        st.markdown("### 예시")
        st.warning("기간, 역명등을 지정하지 않으면 전체를 대상으로 데이터를 필터합니다.")
        st.markdown("1. 하단역")
        st.markdown("2. 1호선 모든 역의 승차데이터를 찾아줘")
        st.markdown("3. 환승역의 지난 1년간 20시부터 22시까지의 승하차 데이터를 찾아줘")
        # TODO: prompt bug
        st.markdown(
            "4. 2022년 1월1일 부터 일주일간 3호선 모든 역과, 하단, 민락, 센텀시티, 서면, 연산, 장전역의 출근시간 승차데이터를 조회해줘")

    st.text_input('아래에 명령어를 입력하세요 👇', key='chatbot_filter_input')
    if st.session_state['chatbot_filter_input']:
        generated_filter = generate_data_filter(
            df, st.session_state['chatbot_filter_input'])
        st.success('✨' + generated_filter['input_summary'])
        st.json(generated_filter)
        st.session_state['chatbot_filter_output'] = generated_filter
        # 인공지능의 아웃풋으로 얻은 json을 세션스테이트에 저장
    else:
        st.session_state['chatbot_filter_output'] = {}
        st.warning('⚠️ 인공지능 필터를 사용하려면 메시지를 입력해주세요.')


def render_sidebar(df):
    with st.sidebar:
        st.sidebar.title("데이터 필터")
        st.write('필터를 선택하세요!')
        st.radio('필터 선택', horizontal=True, options=[
            '일반 필터', '인공지능 필터'], key='filter_selection')
        if st.session_state['filter_selection'] == '일반 필터':
            render_normal_filter(df)

        elif st.session_state['filter_selection'] == '인공지능 필터':
            render_ai_filter(df)

        st.write('💌 seoldonghun@humetro.busan.kr')
        pass
