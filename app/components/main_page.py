import pandas as pd
import numpy as np
import time


def get_dataframe():
    return pd.read_csv(
        "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")


def render_main_page(st):
    st.write(st.session_state)
    st.title('Welcome to Main page')
    st.write(f"Hello {st.session_state['user_info']['username']}")
    st.session_state['df'] = get_dataframe()
    df = st.session_state['df']
    job_filter = st.selectbox("Select the Job", pd.unique(df['job']))
    placeholder = st.empty()

    df = df[df['job'] == job_filter]
    st.session_state['dataframe'] = df
    for second in range(100):
        session_df = st.session_state['dataframe']
        session_df['age_new'] = session_df.loc[:, 'age'] + (second * 1)
        session_df['balance_new'] = session_df.loc[:,
                                                   'balance'] + (second * 1000)

        avg_age = np.mean(session_df['age_new'])

        count_married = int(session_df[(session_df["marital"] == 'married')]
                            ['marital'].count() + second)
        balance = np.mean(session_df['balance_new'])

        with placeholder.container():
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric(label="Age ⏳", value=round(
                avg_age), delta=round(avg_age) - 10)
            kpi2.metric(label="Married Count 💍", value=int(
                count_married), delta=- 10 + count_married)
            kpi3.metric(label="A/C Balance ＄", value=f"$ {round(balance,2)} ",
                        delta=-round(balance/count_married) * 100)
        time.sleep(1)
