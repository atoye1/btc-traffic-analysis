"""
데이터 다운로드를 담당하는 클래스
공공데이터포털에서 데이터를 다운로드하고 로컬에 저장하는 역할
"""

import os
import logging
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

class DataDownloader:
    """
    공공데이터포털에서 부산교통공사 지하철 데이터를 다운로드하는 클래스
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        DataDownloader 초기화
        
        Args:
            config: 설정 파라미터를 담은 딕셔너리
                - base_url: API 기본 URL
                - api_key: 공공데이터포털 API 키
                - download_dir: 데이터를 저장할 경로
        """
        self.config = config or {}
        self.base_url = self.config.get('base_url', 'https://www.data.go.kr/data/3057229/fileData.do')
        self.api_key = self.config.get('api_key', '')
        self.download_dir = self.config.get('download_dir', './data')
        self.logger = logging.getLogger(__name__)
        
        # 다운로드 디렉토리가 없으면 생성
        os.makedirs(self.download_dir, exist_ok=True)
    
    def check_new_data(self) -> List[str]:
        """
        공공데이터포털에서 새로운 데이터가 있는지 확인
        
        Returns:
            새롭게 다운로드해야 할 데이터 파일 목록
        """
        # 이 부분은 실제 API 구현에 맞게 수정 필요
        # 현재는 스텁 구현
        self.logger.info("새로운 데이터를 확인합니다.")
        available_years = self._get_available_years()
        existing_years = self._get_existing_years()
        
        # 새로운 데이터가 있는 연도 목록
        new_years = [year for year in available_years if year not in existing_years]
        
        return new_years
    
    def download_data(self, year: Optional[str] = None) -> str:
        """
        특정 연도의 데이터 다운로드. 연도가 지정되지 않으면 모든 가능한 데이터를 다운로드.
        
        Args:
            year: 다운로드할 데이터의 연도 (예: '2022')
        
        Returns:
            다운로드된 파일 경로
        """
        if year:
            self.logger.info(f"{year}년 데이터를 다운로드합니다.")
            # 특정 연도 데이터만 다운로드
            return self._download_year_data(year)
        else:
            # 모든 새로운 데이터 다운로드
            new_years = self.check_new_data()
            downloaded_files = []
            
            for year in new_years:
                file_path = self._download_year_data(year)
                downloaded_files.append(file_path)
            
            return ', '.join(downloaded_files)
    
    def _download_year_data(self, year: str) -> str:
        """
        특정 연도의 데이터를 다운로드
        
        Args:
            year: 다운로드할 데이터의 연도
            
        Returns:
            다운로드된 파일 경로
        """
        # 실제 구현에서는 requests 등을 사용하여 파일 다운로드 구현
        file_path = os.path.join(self.download_dir, f"{year}.csv")
        
        # 스텁 구현 - 실제로는 아래 코드가 실제 다운로드를 수행해야 함
        # response = requests.get(f"{self.base_url}?year={year}&apiKey={self.api_key}")
        # with open(file_path, 'wb') as f:
        #     f.write(response.content)
        
        self.logger.info(f"{year}년 데이터를 {file_path}에 저장했습니다.")
        return file_path
    
    def _get_available_years(self) -> List[str]:
        """
        공공데이터포털에서 제공하는 사용 가능한 연도 목록을 조회
        
        Returns:
            사용 가능한 연도 목록
        """
        # 실제 구현에서는 API를 호출하여 사용 가능한 연도 목록을 가져옴
        # 현재는 스텁 구현
        current_year = datetime.now().year
        return [str(year) for year in range(2014, current_year + 1)]
    
    def _get_existing_years(self) -> List[str]:
        """
        이미 다운로드된 데이터 파일의 연도 목록을 조회
        
        Returns:
            이미 다운로드된 연도 목록
        """
        existing_files = [f[:-4] for f in os.listdir(self.download_dir) 
                        if f.endswith('.csv') and f[:-4].isdigit()]
        return existing_files
