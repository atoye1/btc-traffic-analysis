# 프로젝트 구조

```
btc-traffic-analysis/
├── legacy/                    # 리팩토링 전 기존 코드
├── src/                       # 소스 코드
│   ├── config/                # 설정 파일
│   ├── data/                  # 데이터 관련 
│   │   ├── downloader/        # 데이터 다운로드 관련
│   │   └── preprocessor/      # 데이터 전처리 관련
│   ├── repository/            # 데이터베이스 접근 레이어
│   ├── pipeline/              # 데이터 파이프라인 관련
│   ├── api/                   # API 서비스 (필요시)
│   └── utils/                 # 유틸리티 기능
├── tests/                     # 테스트 코드
│   ├── unit/                  # 단위 테스트
│   └── integration/           # 통합 테스트
├── notebooks/                 # 데이터 분석 노트북
├── app/                       # 웹 애플리케이션 (Streamlit)
│   └── components/            # UI 컴포넌트
├── scripts/                   # 유틸리티 스크립트
├── data/                      # 데이터 파일 (원본 및 처리된 데이터)
├── docs/                      # 문서
└── alembic/                   # 데이터베이스 마이그레이션 (선택적)
```

## 개발 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Linux/MacOS)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 필요 패키지 설치
pip install -r requirements.txt
```

## 데이터베이스 설정

PostgreSQL을 사용하는 경우:

```bash
# PostgreSQL 설치 (Ubuntu)
sudo apt-get install postgresql postgresql-contrib

# 데이터베이스 생성
createdb btc_traffic_db

# 사용자 생성 및 권한 부여
createuser btc_user
psql -c "ALTER USER btc_user WITH ENCRYPTED PASSWORD 'password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE btc_traffic_db TO btc_user;"
```

## 개발 흐름

1. 테스트 작성
2. 테스트 기반 기능 구현
3. 코드 리뷰 및 리팩토링
4. CI/CD 파이프라인을 통한 자동 테스트 및 배포
