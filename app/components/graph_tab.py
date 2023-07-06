import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from utils.formatters import insert_commas


@st.cache_data(show_spinner='그래프를 렌더링 중입니다.')
def render_graph(df):
    st.write('### 📈 그래프')

    # plt.ticklabel_format(style='plain', axis='x')
    plt.figure(figsize=(10, 10))
    sns.barplot(data=df, y='name',
                x='traffic', estimator='sum', errorbar=None, width=0.5)
    formatter = FuncFormatter(insert_commas)
    plt.gca().xaxis.set_major_formatter(formatter)
    st.pyplot(plt.gcf())
    plt.clf()

    sns.lineplot(data=df.head(100),
                 x=df.head(100).index, y='traffic', hue='name')
    st.pyplot(plt.gcf())


def render_graph_tab(df):
    st.write('그래프가 렌더링 될 예정입니다.')
    pass
