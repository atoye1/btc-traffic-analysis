"""
데이터 파이프라인 모듈

부산교통공사(BTC) 데이터의 다운로드, 전처리, DB 저장을 위한 파이프라인을 제공합니다.
"""
import os
import logging
import pandas as pd
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from src.data.downloader.data_downloader import DataDownloader
from src.data.preprocessor.data_preprocessor import DataPreprocessor
from src.repository.postgres_repository import PostgresRepository

logger = logging.getLogger(__name__)


class DataPipeline:
    """
    데이터 다운로드, 전처리, DB 저장을 위한 파이프라인 클래스
    
    전체 데이터 처리 흐름을 제공합니다.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        DataPipeline 초기화
        
        Args:
            config: 설정 정보 딕셔너리. 다음 키를 포함할 수 있습니다:
                - downloader_config: DataDownloader 설정
                - preprocessor_config: DataPreprocessor 설정
                - db_config: PostgresRepository 설정
        """
        self.config = config or {}
        
        # 컴포넌트 초기화
        self.downloader = DataDownloader(self.config.get('downloader_config', {}))
        self.preprocessor = DataPreprocessor(self.config.get('preprocessor_config', {}))
        self.repository = PostgresRepository(self.config.get('db_config', {}))
        
        # 스케줄러 초기화
        self.scheduler = BackgroundScheduler()
        
    def run(self, years: List[str] = None) -> bool:
        """
        전체 파이프라인을 실행합니다.
        
        Args:
            years: 처리할 특정 연도 목록 (None인 경우 모든 새로운 데이터 처리)
            
        Returns:
            bool: 실행 성공 여부
        """
        try:
            logger.info("Starting data pipeline")
            
            # 1. 데이터 다운로드
            if years:
                downloaded_files = []
                for year in years:
                    downloaded_files.extend(self.downloader.download_data(year))
            else:
                downloaded_files = self.downloader.download_data()
            
            if not downloaded_files:
                logger.info("No new data to process")
                return True
            
            logger.info(f"Downloaded {len(downloaded_files)} files: {downloaded_files}")
            
            # 2. 데이터 전처리
            processed_data = self.preprocessor.preprocess(downloaded_files)
            
            if processed_data.empty:
                logger.warning("No data after preprocessing")
                return False
            
            logger.info(f"Preprocessed data: {processed_data.shape[0]} rows")
            
            # 3. DB 저장
            self.repository.connect()
            save_result = self.repository.save_dataframe(processed_data)
            self.repository.close()
            
            if not save_result:
                logger.error("Failed to save data to database")
                return False
            
            logger.info("Data pipeline completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error running data pipeline: {e}")
            return False
    
    def schedule(self, cron_expression: str = '0 0 1 * *') -> None:
        """
        파이프라인 실행을 스케줄링합니다. 기본값은 매월 1일 00:00에 실행.
        
        Args:
            cron_expression: cron 표현식 (기본값: 매월 1일 자정)
        """
        self.scheduler.add_job(self.run, 'cron', **self._parse_cron(cron_expression))
        self.scheduler.start()
        logger.info(f"Scheduled pipeline with cron expression: {cron_expression}")
    
    def stop_scheduler(self) -> None:
        """스케줄러를 중지합니다."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def _parse_cron(self, cron_expression: str) -> Dict[str, int]:
        """
        cron 표현식을 파싱하여 스케줄러 매개변수로 변환합니다.
        
        Args:
            cron_expression: cron 표현식 (예: '0 0 1 * *' - 매월 1일 자정)
            
        Returns:
            Dict[str, int]: 스케줄러 매개변수
        """
        parts = cron_expression.split()
        
        if len(parts) != 5:
            logger.warning(f"Invalid cron expression: {cron_expression}, using default")
            return {'hour': 0, 'day': 1}
        
        minute, hour, day, month, day_of_week = parts
        
        result = {}
        
        if minute != '*':
            result['minute'] = int(minute)
        
        if hour != '*':
            result['hour'] = int(hour)
        
        if day != '*':
            result['day'] = int(day)
        
        if month != '*':
            result['month'] = int(month)
        
        if day_of_week != '*':
            result['day_of_week'] = int(day_of_week)
        
        return result
    
    def process_batch(self, start_date: str, end_date: str) -> bool:
        """
        특정 날짜 범위의 데이터를 처리합니다.
        
        Args:
            start_date: 시작 날짜 (YYYY-MM-DD 형식)
            end_date: 종료 날짜 (YYYY-MM-DD 형식)
            
        Returns:
            bool: 처리 성공 여부
        """
        try:
            logger.info(f"Processing batch: {start_date} to {end_date}")
            
            # 날짜 범위에 해당하는 연도 목록 생성
            start_year = datetime.strptime(start_date, '%Y-%m-%d').year
            end_year = datetime.strptime(end_date, '%Y-%m-%d').year
            years = [str(year) for year in range(start_year, end_year + 1)]
            
            return self.run(years)
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            return False
    
    def process_latest(self) -> bool:
        """
        최신 데이터를 처리합니다 (현재 연도).
        
        Returns:
            bool: 처리 성공 여부
        """
        current_year = str(datetime.now().year)
        return self.run([current_year])
    
    def process_all(self) -> bool:
        """
        모든 기존 데이터를 처리합니다 (전체 재처리).
        
        Returns:
            bool: 처리 성공 여부
        """
        return self.run()
