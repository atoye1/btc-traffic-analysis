import pickle
import pandas as pd
import glob
import os
import numpy as np


def raw_data_preprocessor(df_raw):
    df_result = df_raw.copy().dropna(axis=0)
    df_result = drop_missing_rows(df_result)
    df_result = remove_string_whitespaces(df_result)
    df_result = drop_day_col(df_result)
    df_result = process_date(df_result)
    df_result = cast_float_to_int(df_result)
    df_result = replace_tilda_in_column(df_result)
    df_result = replace_on_off_bool(df_result)
    df_checker(df_result)
    return df_result


def drop_missing_rows(df, threshhold=12):
    # 역번호 기준으로 필터링
    # 역명 기준으로 필터링한다.
    # 먼저 역번호 기준으로 평균 레코드 수는 730개 정도 된다.
    # 평균보다 현저히 작은 갯수의 레코드는 날린다.
    # 1년이 12일이니깐 이거보다 작은 데이터는 날린다.
    for station_number in df['역번호'].unique():
        if len(df[df['역번호'] == station_number]) < threshhold:
            print(station_number)
            df = df.copy().drop(df[df['역번호'] == station_number].index)
    for station_name in df['역명'].unique():
        if len(df[df['역명'] == station_name]) < threshhold:
            print(station_name)
            df = df.copy().drop(df[df['역명'] == station_name].index)
    return df


def process_date(df):
    if df['년월일'].dtype == 'object':
        df['년월일'] = df['년월일'].str.replace('-', '').replace('.', '')
        df['년월일'] = df['년월일'].copy().astype(int)
    return df


def df_checker(df):
    assert df.shape[0] > 30000
    assert df.shape[1] == 29
    assert sum(df.isna().sum()) == 0
    for col_name in df.columns:
        # added 'bool' to the list of accepted dtypes
        if df[col_name].dtype not in ['object', 'int32', 'bool']:
            raise Exception(f'Invalid column dtype {df[col_name].dtype}')


def replace_tilda_in_column(df):
    for col_name in df.columns:
        if '~' in col_name:
            new_col_name = col_name.replace('~', '-')
            df[new_col_name] = df[col_name]
            df = df.drop(col_name, axis=1)
    return df


def replace_on_off_bool(df):
    df['구분'] = df['구분'].copy().map(lambda x: x == '승차')
    df['구분'] = df['구분'].astype(bool)
    print(df.dtypes)
    return df


def remove_string_whitespaces(df):
    for col_name in df.columns:
        if df[col_name].dtype == 'object':
            df[col_name] = df[col_name].map(
                lambda x: x.replace(' ', '').strip()).copy()
    return df


# 역번호, 년월일, 합계, 시점별 탑승량이 float으로 되어있으므로 int로 변경해준다.
# 결측치, NaN을 제거한 후 적용해야 한다.
def cast_float_to_int(df):
    for col_name in df.columns:
        if df[col_name].dtype == 'float' or df[col_name].dtype == 'int64':
            df[col_name] = df[col_name].astype('int32').copy()
    return df


def drop_day_col(df):
    try:
        df = df.copy().drop('요일', axis=1)
    except KeyError:
        # '요일이 없는 경우 KeyError 발생하는데, 이건 정상적인 에러'
        pass
    return df


# concat every dfs
def concat_melt_dfs(df_list):
    df_concated = pd.concat(df_list)
    df_melted = df_concated.melt(id_vars=['역번호', '역명', '년월일', '구분'], value_vars=['01시-02시', '02시-03시', '03시-04시',
                                                                                 '04시-05시', '05시-06시', '06시-07시', '07시-08시', '08시-09시', '09시-10시',
                                                                                 '10시-11시', '11시-12시', '12시-13시', '13시-14시', '14시-15시', '15시-16시',
                                                                                 '16시-17시', '17시-18시', '18시-19시', '19시-20시', '20시-21시', '21시-22시',
                                                                                 '22시-23시', '23시-24시', '24시-01시'])
    df_melted['hour'] = df_melted['variable'].str.slice(0, 2).astype(int)
    df_melted['timestamp'] = pd.to_datetime(
        df_melted['년월일'], format='%Y%m%d') + pd.to_timedelta(df_melted['hour'], unit='h')
    df_melted.drop(columns=['년월일', 'variable', 'hour'], inplace=True)
    df_melted.rename(columns={'value': 'passenger_count'}, inplace=True)

    df_melted.sort_values(['timestamp', '역번호'], inplace=True)
    result = df_melted.reset_index()
    result = result.drop('index', axis=1)
    result.columns = ['id', 'name', 'on', 'traffic', 'timestamp']

    # timestamp를 인덱스로 지정해준다
    result.set_index('timestamp', inplace=True)

    # 동부산대 역이 윗반송으로 변경되었다.
    # 동부산대를 없애고 윗반송으로 대체해준다.
    result.loc[result['name'] == '동부산대', 'name'] = '윗반송'
    assert result['name'].nunique() == result['id'].nunique(
    ), f"두 컬럼의 고유값은 동일해야 한다. {result['name'].nunique()} {result['id'].nunique()}"
    return result


def ingest_csv_files():
    csv_files = glob.glob('./data/2*.csv')
    print(csv_files)
    csv_files.sort()
    df_list = []
    for csv_file in csv_files:
        df_raw = pd.read_csv(csv_file, encoding='cp949')
        df_p = raw_data_preprocessor(df_raw)
        df_list.append(df_p)
    df_cleaned = concat_melt_dfs(df_list)

    with open('./data/df_cleaned.pkl', 'wb') as f:
        pickle.dump(df_cleaned, f)


ingest_csv_files()
