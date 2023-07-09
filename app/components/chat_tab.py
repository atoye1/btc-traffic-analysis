import streamlit as st
from streamlit_chat import message

# Initialise session state variables

model_name = "GPT-3.5"


def generate_response(prompt):
    # st.session_state['messages'].append({"role": "user", "content": prompt})

    # completion = openai.ChatCompletion.create(
    #     model=model,
    #     messages=st.session_state['messages']
    # )
    # response = completion.choices[0].message.content
    # st.session_state['messages'].append({"role": "assistant", "content": response})

    # # print(st.session_state['messages'])
    # total_tokens = completion.usage.total_tokens
    # prompt_tokens = completion.usage.prompt_tokens
    # completion_tokens = completion.usage.completion_tokens
    return '채팅 기능은 아직 구현되지 않았습니다.', 100, 100, 100


def render_chat_tab(df):

    st.write('### 🤖 챗봇에게 질문하기')
    st.info('왼쪽에 표시된 데이터에 대해 챗봇에게 물어보세요!')
    # container for chat history
    response_container = st.container()

    # container for text box
    container = st.container()
    with container:
        # with st.form(key='my_form', clear_on_submit=True):
        #     submit_button = st.form_submit_button(label='Send')

        user_input = st.text_input("질문하기:", key='input')
        if user_input:
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(
                user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
            st.session_state['model_name'].append(model_name)
            st.session_state['total_tokens'].append(total_tokens)

            # from https://openai.com/pricing#language-models
            if model_name == "GPT-3.5":
                cost = total_tokens * 0.002 / 1000
            else:
                cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

            st.session_state['cost'].append(cost)
            st.session_state['total_cost'] += cost

        if st.session_state['generated']:
            with response_container:

                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i],
                            is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))

    clear_button = st.button("Clear chat history")
    if clear_button:
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.session_state['number_tokens'] = []
        st.session_state['model_name'] = []
        st.session_state['cost'] = []
        st.session_state['total_cost'] = 0.0
        st.session_state['total_tokens'] = []
