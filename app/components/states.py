def init_states(st):
    if "user_info" not in st.session_state:
        print('initialzing user info')
        st.session_state["user_info"] = {
            "username": "",
            "logged_in": False
        }
        # 채팅 기록을 저장할 리스트

    if "chat_history" not in st.session_state:
        print('initialzing chat history')
        st.session_state["chat_history"] = []

    if "df" not in st.session_state:
        print('initialzing df')
        st.session_state["df"] = object()
