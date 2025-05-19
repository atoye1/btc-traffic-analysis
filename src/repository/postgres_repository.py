"""
PostgreSQL 데이터베이스 리포지토리 모듈

부산교통공사(BTC) 데이터의 DB 저장 및 조회 기능을 제공합니다.
"""
import os
import logging
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, DateTime, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional, Union, Any, Tuple

logger = logging.getLogger(__name__)
Base = declarative_base()


class TrafficData(Base):
    """교통 데이터 테이블 정의"""
    __tablename__ = 'traffic_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, nullable=False, index=True)
    station_name = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    on_off = Column(Boolean, nullable=False)  # True: 승차, False: 하차
    passenger_count = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<TrafficData(id={self.id}, station_id={self.station_id}, station_name='{self.station_name}', timestamp='{self.timestamp}', on_off={self.on_off}, passenger_count={self.passenger_count})>"


class StationMetadata(Base):
    """역 메타데이터 테이블 정의"""
    __tablename__ = 'station_metadata'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    line = Column(String(20), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<StationMetadata(id={self.id}, name='{self.name}', line='{self.line}', lat={self.latitude}, lon={self.longitude})>"


class PostgresRepository:
    """
    PostgreSQL 데이터베이스 접근을 위한 리포지토리 클래스
    
    데이터의 저장, 조회, 업데이트, 삭제 기능을 제공합니다.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        PostgresRepository 초기화
        
        Args:
            config: 설정 정보 딕셔너리. 다음 키를 포함할 수 있습니다:
                - host: 데이터베이스 호스트
                - port: 데이터베이스 포트
                - username: 데이터베이스 사용자 이름
                - password: 데이터베이스 비밀번호
                - database: 데이터베이스 이름
                - connection_string: 직접 연결 문자열 (다른 설정보다 우선)
        """
        self.config = config or {}
        
        # 연결 문자열이 직접 제공되었는지 확인
        if 'connection_string' in self.config:
            self.connection_string = self.config['connection_string']
        else:
            # 기본값 사용 또는 설정에서 값 가져오기
            host = self.config.get('host', 'localhost')
            port = self.config.get('port', 5432)
            username = self.config.get('username', 'postgres')
            password = self.config.get('password', 'postgres')
            database = self.config.get('database', 'btc_traffic_db')
            
            self.connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        
        self.engine = None
        self.Session = None
    
    def connect(self) -> None:
        """데이터베이스 연결을 설정합니다."""
        try:
            self.engine = create_engine(self.connection_string)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def close(self) -> None:
        """데이터베이스 연결을 종료합니다."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def save_dataframe(self, df: pd.DataFrame, table_name: str = 'traffic_data', if_exists: str = 'append') -> bool:
        """
        데이터프레임을 데이터베이스 테이블에 저장합니다.
        
        Args:
            df: 저장할 데이터프레임
            table_name: 저장할 테이블 이름
            if_exists: 테이블이 이미 존재하는 경우의 처리 방식 ('fail', 'replace', 'append')
            
        Returns:
            bool: 저장 성공 여부
        """
        if not self.engine:
            self.connect()
        
        try:
            # 데이터프레임 전처리
            if table_name == 'traffic_data':
                # TrafficData 테이블에 맞게 데이터 변환
                df_to_save = df.reset_index()
                df_to_save.rename(columns={
                    'id': 'station_id',
                    'name': 'station_name',
                    'timestamp': 'timestamp',
                    'on': 'on_off',
                    'traffic': 'passenger_count'
                }, inplace=True)
            elif table_name == 'station_metadata':
                # StationMetadata 테이블에 맞게 데이터 변환
                df_to_save = df.copy()
            else:
                df_to_save = df.copy()
            
            # 데이터베이스에 저장
            df_to_save.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Saved dataframe to table {table_name}: {len(df_to_save)} rows")
            return True
        except Exception as e:
            logger.error(f"Error saving dataframe to table {table_name}: {e}")
            return False
    
    def get_latest_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        최신 데이터를 조회합니다.
        
        Args:
            filters: 조회 필터 (역, 날짜 범위 등)
            
        Returns:
            pd.DataFrame: 조회된 데이터
        """
        if not self.engine:
            self.connect()
        
        filters = filters or {}
        query = "SELECT * FROM traffic_data"
        
        # 필터 조건 추가
        where_clauses = []
        params = {}
        
        if 'station_id' in filters:
            where_clauses.append("station_id = :station_id")
            params['station_id'] = filters['station_id']
        
        if 'station_name' in filters:
            where_clauses.append("station_name = :station_name")
            params['station_name'] = filters['station_name']
        
        if 'start_date' in filters:
            where_clauses.append("timestamp >= :start_date")
            params['start_date'] = filters['start_date']
        
        if 'end_date' in filters:
            where_clauses.append("timestamp <= :end_date")
            params['end_date'] = filters['end_date']
        
        if 'on_off' in filters:
            where_clauses.append("on_off = :on_off")
            params['on_off'] = filters['on_off']
        
        # WHERE 절 추가
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        # 정렬 추가
        query += " ORDER BY timestamp DESC"
        
        # 제한 추가
        if 'limit' in filters:
            query += " LIMIT :limit"
            params['limit'] = filters['limit']
        
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error querying latest data: {e}")
            return pd.DataFrame()
    
    def get_data_by_date_range(self, start_date: str, end_date: str, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        날짜 범위로 데이터를 조회합니다.
        
        Args:
            start_date: 시작 날짜 (YYYY-MM-DD 형식)
            end_date: 종료 날짜 (YYYY-MM-DD 형식)
            filters: 추가 필터
            
        Returns:
            pd.DataFrame: 조회된 데이터
        """
        filters = filters or {}
        filters['start_date'] = start_date
        filters['end_date'] = end_date
        return self.get_latest_data(filters)
    
    def get_data_by_station(self, station_name: str, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        특정 역의 데이터를 조회합니다.
        
        Args:
            station_name: 역 이름
            filters: 추가 필터
            
        Returns:
            pd.DataFrame: 조회된 데이터
        """
        filters = filters or {}
        filters['station_name'] = station_name
        return self.get_latest_data(filters)
    
    def get_station_metadata(self, station_name: Optional[str] = None, line: Optional[str] = None) -> pd.DataFrame:
        """
        역 메타데이터를 조회합니다.
        
        Args:
            station_name: 역 이름 (None인 경우 모든 역)
            line: 노선 (None인 경우 모든 노선)
            
        Returns:
            pd.DataFrame: 조회된 메타데이터
        """
        if not self.engine:
            self.connect()
        
        query = "SELECT * FROM station_metadata"
        params = {}
        
        # 필터 조건 추가
        where_clauses = []
        
        if station_name:
            where_clauses.append("name = :station_name")
            params['station_name'] = station_name
        
        if line:
            where_clauses.append("line = :line")
            params['line'] = line
        
        # WHERE 절 추가
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error querying station metadata: {e}")
            return pd.DataFrame()
    
    def get_all_lines(self) -> List[str]:
        """
        모든 노선 목록을 조회합니다.
        
        Returns:
            List[str]: 노선 목록
        """
        if not self.engine:
            self.connect()
        
        query = "SELECT DISTINCT line FROM station_metadata ORDER BY line"
        
        try:
            df = pd.read_sql(query, self.engine)
            return df['line'].tolist()
        except Exception as e:
            logger.error(f"Error querying all lines: {e}")
            return []
    
    def get_stations_by_line(self, line: str) -> List[str]:
        """
        특정 노선의 역 목록을 조회합니다.
        
        Args:
            line: 노선
            
        Returns:
            List[str]: 역 목록
        """
        if not self.engine:
            self.connect()
        
        query = "SELECT name FROM station_metadata WHERE line = :line ORDER BY name"
        params = {'line': line}
        
        try:
            df = pd.read_sql(query, self.engine, params=params)
            return df['name'].tolist()
        except Exception as e:
            logger.error(f"Error querying stations by line: {e}")
            return []
    
    def get_aggregated_data(self, group_by: str, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        데이터를 특정 기준으로 집계합니다.
        
        Args:
            group_by: 집계 기준 ('hour', 'day', 'month', 'station', 'line')
            filters: 조회 필터
            
        Returns:
            pd.DataFrame: 집계된 데이터
        """
        if not self.engine:
            self.connect()
        
        filters = filters or {}
        
        # 집계 쿼리 생성
        select_clause = ""
        group_by_clause = ""
        
        if group_by == 'hour':
            select_clause = "EXTRACT(HOUR FROM timestamp) AS hour, SUM(passenger_count) AS total_passengers"
            group_by_clause = "EXTRACT(HOUR FROM timestamp)"
            order_by_clause = "hour"
        elif group_by == 'day':
            select_clause = "DATE(timestamp) AS day, SUM(passenger_count) AS total_passengers"
            group_by_clause = "DATE(timestamp)"
            order_by_clause = "day"
        elif group_by == 'month':
            select_clause = "EXTRACT(YEAR FROM timestamp) AS year, EXTRACT(MONTH FROM timestamp) AS month, SUM(passenger_count) AS total_passengers"
            group_by_clause = "EXTRACT(YEAR FROM timestamp), EXTRACT(MONTH FROM timestamp)"
            order_by_clause = "year, month"
        elif group_by == 'station':
            select_clause = "station_name, SUM(passenger_count) AS total_passengers"
            group_by_clause = "station_name"
            order_by_clause = "total_passengers DESC"
        elif group_by == 'line':
            select_clause = """
                sm.line, 
                SUM(td.passenger_count) AS total_passengers
            """
            from_clause = """
                traffic_data td
                JOIN station_metadata sm ON td.station_name = sm.name
            """
            group_by_clause = "sm.line"
            order_by_clause = "total_passengers DESC"
        else:
            logger.error(f"Invalid group_by parameter: {group_by}")
            return pd.DataFrame()
        
        # 기본 쿼리
        if group_by == 'line':
            query = f"SELECT {select_clause} FROM {from_clause}"
        else:
            query = f"SELECT {select_clause} FROM traffic_data"
        
        # 필터 조건 추가
        where_clauses = []
        params = {}
        
        if 'station_id' in filters:
            where_clauses.append("station_id = :station_id")
            params['station_id'] = filters['station_id']
        
        if 'station_name' in filters:
            where_clauses.append("station_name = :station_name")
            params['station_name'] = filters['station_name']
        
        if 'start_date' in filters:
            where_clauses.append("timestamp >= :start_date")
            params['start_date'] = filters['start_date']
        
        if 'end_date' in filters:
            where_clauses.append("timestamp <= :end_date")
            params['end_date'] = filters['end_date']
        
        if 'on_off' in filters:
            where_clauses.append("on_off = :on_off")
            params['on_off'] = filters['on_off']
        
        # WHERE 절 추가
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        # GROUP BY 및 ORDER BY 절 추가
        query += f" GROUP BY {group_by_clause} ORDER BY {order_by_clause}"
        
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error querying aggregated data: {e}")
            return pd.DataFrame()
