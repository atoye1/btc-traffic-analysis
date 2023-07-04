import pandas as pd
import base64
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit as st


"""
1. csv
2. xlsx
3. hwp
4. image
5. pdf
"""

# TODO: 파일 바이너리 포팅과 컴포턴트 렌더링을 분리해야 한다.


def to_csv(df: pd.DataFrame):
    file_binary = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(file_binary.encode()).decode()
    st.download_button(label='Download CSV File', data=file_binary,
                       file_name='playerstats.csv', mime='text/csv')


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()

    df_xlsx = processed_data
    st.download_button(label='📥 Download Excel File',
                       data=df_xlsx,
                       file_name='df_test.xlsx')
