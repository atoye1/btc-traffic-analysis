from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    with st.expander('필터 적용하기'):
        df = df.copy()
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass
            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize()
        modification_container = st.container()

        with modification_container:
            st.write('필터를 선택해주세요')
            to_filter_column = st.multiselect(
                "Filter Dataframe on", df.columns)
            for column in to_filter_column:
                left, right = st.columns((5, 20))
                left.write(column)
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]

                elif is_numeric_dtype(df[column]):
                    if df[column].dtypes == 'int64':
                        # int
                        _min = int(df[column].min())
                        _max = int(df[column].max())
                        step = 1
                    else:
                        # float
                        _min = float(df[column].min())
                        _max = float(df[column].max())
                        step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(
                            str).str.contains(user_text_input)]

    return df
