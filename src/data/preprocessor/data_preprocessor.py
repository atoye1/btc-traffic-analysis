"""
데이터 전처리기 모듈

부산교통공사(BTC) 데이터의 전처리 기능을 제공합니다.
"""
import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    부산교통공사(BTC) 데이터 전처리를 위한 클래스
    
    원본 CSV 데이터를 읽고 정제, 변환, 병합하는 기능을 제공합니다.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        DataPreprocessor 초기화
        
        Args:
            config: 설정 정보 딕셔너리. 다음 키를 포함할 수 있습니다:
                - input_dir: 원본 데이터가 있는 디렉토리 경로
                - output_dir: 전처리된 데이터를 저장할 디렉토리 경로
                - threshold: 결측값 처리 임계값
        """
        self.config = config or {}
        self.input_dir = self.config.get('input_dir', './data')
        self.output_dir = self.config.get('output_dir', './data/processed')
        self.threshold = self.config.get('threshold', 12)
        
        # 출력 디렉토리가 없으면 생성
        os.makedirs(self.output_dir, exist_ok=True)
    
    def preprocess(self, file_paths: List[str] = None) -> pd.DataFrame:
        """
        전체 전처리 프로세스를 실행합니다.
        
        Args:
            file_paths: 전처리할 CSV 파일 경로 목록. None인 경우 input_dir의 모든 CSV 파일 처리
            
        Returns:
            pd.DataFrame: 전처리된 데이터프레임
        """
        if file_paths is None:
            file_paths = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) 
                         if f.endswith('.csv') and f.split('.')[0].isdigit()]
        
        logger.info(f"Processing {len(file_paths)} files")
        
        # 각 파일 전처리
        df_list = []
        for file_path in sorted(file_paths):
            try:
                df_raw = pd.read_csv(file_path, encoding='cp949')
                df_processed = self.process_raw_data(df_raw)
                df_list.append(df_processed)
                logger.info(f"Processed file: {file_path}")
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
        
        # 데이터프레임 결합 및 변환
        if df_list:
            df_combined = self.combine_data_frames(df_list)
            # 결과 저장
            output_path = os.path.join(self.output_dir, "btc_traffic_data_processed.pickle")
            df_combined.to_pickle(output_path)
            logger.info(f"Saved processed data to {output_path}")
            return df_combined
        
        return pd.DataFrame()
    
    def process_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        원본 데이터프레임을 전처리합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 전처리된 데이터프레임
        """
        df_result = df.copy().dropna(axis=0)
        df_result = self.drop_missing_rows(df_result)
        df_result = self.remove_string_whitespaces(df_result)
        df_result = self.drop_day_col(df_result)
        df_result = self.process_date(df_result)
        df_result = self.cast_float_to_int(df_result)
        df_result = self.replace_tilda_in_column(df_result)
        df_result = self.replace_on_off_bool(df_result)
        self.validate_dataframe(df_result)
        return df_result
    
    def drop_missing_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        역번호/역명 기준으로 불필요한 행을 제거합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        # 특정 역번호/역명이 threshold 이하인 행은 제거
        for station_number in df['역번호'].unique():
            if len(df[df['역번호'] == station_number]) < self.threshold:
                df = df.copy().drop(df[df['역번호'] == station_number].index)
        
        for station_name in df['역명'].unique():
            if len(df[df['역명'] == station_name]) < self.threshold:
                df = df.copy().drop(df[df['역명'] == station_name].index)
        
        return df
    
    def process_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        날짜 형식을 정규화합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 날짜가 처리된 데이터프레임
        """
        if df['날짜'].dtype == 'object':
            df['날짜'] = df['날짜'].str.replace('-', '').replace('.', '')
            df['날짜'] = df['날짜'].copy().astype(int)
        return df
    
    def validate_dataframe(self, df: pd.DataFrame) -> None:
        """
        데이터프레임 유효성을 검증합니다.
        
        Args:
            df: 검증할 데이터프레임
            
        Raises:
            Exception: 유효성 검사 실패 시
        """
        assert df.shape[0] > 30000, "데이터프레임의 행 수가 너무 적습니다."
        assert df.shape[1] == 29, "데이터프레임의 열 수가 올바르지 않습니다."
        assert sum(df.isna().sum()) == 0, "누락된 값이 존재합니다."
        
        for col_name in df.columns:
            if df[col_name].dtype not in ['object', 'int32', 'bool']:
                raise Exception(f'Invalid column dtype {df[col_name].dtype}')
    
    def replace_tilda_in_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        열 이름의 물결표(~)를 대시(-)로 변경합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 열 이름이 변경된 데이터프레임
        """
        for col_name in df.columns:
            if '~' in col_name:
                new_col_name = col_name.replace('~', '-')
                df[new_col_name] = df[col_name]
                df = df.drop(col_name, axis=1)
        return df
    
    def replace_on_off_bool(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        승하차 구분을 불리언 값으로 변환합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 변환된 데이터프레임
        """
        df['구분'] = df['구분'].copy().map(lambda x: x == '승차')
        df['구분'] = df['구분'].astype(bool)
        return df
    
    def remove_string_whitespaces(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        문자열 열의 공백을 제거합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 공백이 제거된 데이터프레임
        """
        for col_name in df.columns:
            if df[col_name].dtype == 'object':
                df[col_name] = df[col_name].map(
                    lambda x: x.replace(' ', '').strip()).copy()
        return df
    
    def cast_float_to_int(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        float 형식의 열을 int로 변환합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 변환된 데이터프레임
        """
        for col_name in df.columns:
            if df[col_name].dtype == 'float' or df[col_name].dtype == 'int64':
                df[col_name] = df[col_name].astype('int32').copy()
        return df
    
    def drop_day_col(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        요일 열을 제거합니다.
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pd.DataFrame: 요일 열이 제거된 데이터프레임
        """
        try:
            df = df.copy().drop('요일', axis=1)
        except KeyError:
            # 요일이 없는 경우 KeyError 무시
            pass
        return df
    
    def combine_data_frames(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        """
        여러 데이터프레임을 결합하고 변환합니다.
        
        Args:
            df_list: 결합할 데이터프레임 목록
            
        Returns:
            pd.DataFrame: 결합 및 변환된 데이터프레임
        """
        # 데이터프레임 결합
        df_concatenated = pd.concat(df_list)
        
        # 시간대별 데이터를 행으로 변환 (melt)
        time_columns = [
            '01시-02시', '02시-03시', '03시-04시', '04시-05시', '05시-06시', 
            '06시-07시', '07시-08시', '08시-09시', '09시-10시', '10시-11시', 
            '11시-12시', '12시-13시', '13시-14시', '14시-15시', '15시-16시', 
            '16시-17시', '17시-18시', '18시-19시', '19시-20시', '20시-21시', 
            '21시-22시', '22시-23시', '23시-24시', '24시-01시'
        ]
        
        df_melted = df_concatenated.melt(
            id_vars=['역번호', '역명', '날짜', '구분'],
            value_vars=time_columns
        )
        
        # 시간 정보 추출
        df_melted['hour'] = df_melted['variable'].str.slice(0, 2).astype(int)
        
        # 타임스탬프 생성
        df_melted['timestamp'] = pd.to_datetime(
            df_melted['날짜'], format='%Y%m%d') + pd.to_timedelta(df_melted['hour'], unit='h')
        
        # 불필요한 열 제거
        df_melted.drop(columns=['날짜', 'variable', 'hour'], inplace=True)
        
        # 열 이름 변경
        df_melted.rename(columns={'value': 'passenger_count'}, inplace=True)
        
        # 정렬 및 인덱스 재설정
        df_melted.sort_values(['timestamp', '역번호'], inplace=True)
        result = df_melted.reset_index()
        result = result.drop('index', axis=1)
        
        # 열 이름 변경
        result.columns = ['id', 'name', 'on', 'traffic', 'timestamp']
        
        # 타임스탬프를 인덱스로 설정
        result.set_index('timestamp', inplace=True)
        
        # '부전역'과 '서면' 통일
        result.loc[result['name'] == '부전역', 'name'] = '서면'
        
        return result
