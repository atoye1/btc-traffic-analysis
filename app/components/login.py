import streamlit


def render_login(st: streamlit):
    st.title("Login First")
    st.write(st.session_state)
    with st.form(key="login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.session_state["user_info"] = {
                "username": username,
                "logged_in": True,
            }
            st.experimental_rerun()
