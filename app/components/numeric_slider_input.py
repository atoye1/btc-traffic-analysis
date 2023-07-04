import streamlit as st


def render_numeric_slider_input():

    if not st.session_state.get('sep_len_text'):
        st.session_state['sep_len_text'] = 5

    if not st.session_state.get('sep_len_slider'):
        st.session_state['sep_len_slider'] = 5

    def update_slider():
        st.session_state.sep_len_slider = st.session_state.sep_len_text

    def update_numeric():
        st.session_state.sep_len_text = st.session_state.sep_len_slider

    sepal_length_text = st.number_input("Sepal Length",
                                        min_value=4.3, max_value=7.9,
                                        value=5.5, on_change=update_slider, key='sep_len_text')

    sepal_length_slider = st.slider("Sepal Length", min_value=4.3, max_value=7.9,
                                    step=0.1,
                                    value=5.5,
                                    on_change=update_numeric, key='sep_len_slider')
