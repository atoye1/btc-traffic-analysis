"""
데이터 다운로더 모듈

부산교통공사(BTC) 데이터를 공공데이터포털에서 다운로드하는 기능을 제공합니다.
"""
import os
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger(__name__)


class DataDownloader:
    """
    공공데이터포털에서 부산교통공사(BTC) 데이터를 다운로드하는 클래스
    
    새로운 데이터가 추가되었는지 확인하고, 필요한 경우 다운로드합니다.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        DataDownloader 초기화
        
        Args:
            config: 설정 정보 딕셔너리. 다음 키를 포함할 수 있습니다:
                - api_key: 공공데이터포털 API 키
                - base_url: API 기본 URL
                - data_dir: 다운로드한 데이터를 저장할 디렉토리 경로
        """
        self.config = config or {}
        self.api_key = self.config.get('api_key', os.environ.get('DATA_GO_KR_API_KEY', ''))
        self.base_url = self.config.get('base_url', 'https://www.data.go.kr/api/3057229')
        self.data_dir = self.config.get('data_dir', './data')
        
        # 데이터 디렉토리가 없으면 생성
        os.makedirs(self.data_dir, exist_ok=True)
        
    def check_new_data(self) -> List[str]:
        """
        공공데이터포털에 새로운 데이터가 추가되었는지 확인합니다.
        
        Returns:
            List[str]: 새로 추가된 데이터의 연도 목록
        """
        # TODO: 실제 API 호출 및 데이터 비교 로직 구현
        logger.info("Checking for new data on the portal")
        
        # 임시 로직 (구현 필요)
        available_years = self._get_available_years()
        downloaded_years = self._get_downloaded_years()
        
        return [year for year in available_years if year not in downloaded_years]
    
    def download_data(self, year: Optional[str] = None) -> List[str]:
        """
        공공데이터포털에서 데이터를 다운로드합니다.
        
        Args:
            year: 다운로드할 특정 연도 (None인 경우 모든 새로운 데이터 다운로드)
            
        Returns:
            List[str]: 다운로드된 파일 경로 목록
        """
        # TODO: 실제 API 호출 및 데이터 다운로드 로직 구현
        logger.info(f"Downloading data for year: {year if year else 'all new data'}")
        
        if year:
            years_to_download = [year]
        else:
            years_to_download = self.check_new_data()
            
        downloaded_files = []
        for year_to_download in years_to_download:
            file_path = self._download_year_data(year_to_download)
            if file_path:
                downloaded_files.append(file_path)
        
        return downloaded_files
    
    def _get_available_years(self) -> List[str]:
        """공공데이터포털에서 사용 가능한 연도 목록을 가져옵니다."""
        # TODO: 실제 API 호출 로직 구현
        # 임시 로직 (구현 필요)
        return ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
    
    def _get_downloaded_years(self) -> List[str]:
        """이미 다운로드된 연도 목록을 가져옵니다."""
        # 데이터 디렉토리의 CSV 파일을 기준으로 다운로드된 연도 파악
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv') and f.split('.')[0].isdigit()]
        return [f.split('.')[0] for f in files]
    
    def _download_year_data(self, year: str) -> Optional[str]:
        """
        특정 연도의 데이터를 다운로드합니다.
        
        Args:
            year: 다운로드할 연도
            
        Returns:
            Optional[str]: 다운로드된 파일 경로 또는 실패 시 None
        """
        # TODO: 실제 API 호출 및 파일 다운로드 로직 구현
        target_file = os.path.join(self.data_dir, f"{year}.csv")
        
        # 임시 로직 (구현 필요)
        logger.info(f"Downloading data for year {year} to {target_file}")
        return target_file if os.path.exists(target_file) else None
