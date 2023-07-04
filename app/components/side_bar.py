import time


def render_side_bar(st):
    st.sidebar.markdown("### Chat Module")
    # 채팅 기록 표시
    for chat_message in st.session_state['chat_history']:
        st.sidebar.markdown(f"> {chat_message}")

    # 채팅 입력 및 전송 버튼
    user_message = st.sidebar.text_input("Enter your message:")
    if st.sidebar.button("Send"):
        st.session_state['chat_history'].append(user_message)
        st.sidebar.text_input("Enter your message:", value="")
