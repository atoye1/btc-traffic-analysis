# 프로젝트 구조

```
btc-traffic-analysis/
├── legacy/                   # 기존 코드 보관
├── src/                      # 소스 코드
│   ├── download/             # 데이터 다운로드 관련 코드
│   │   ├── __init__.py
│   │   ├── downloader.py
│   │   └── api_client.py
│   ├── preprocess/           # 데이터 전처리 관련 코드
│   │   ├── __init__.py
│   │   └── preprocessor.py
│   ├── repository/           # 데이터베이스 관련 코드
│   │   ├── __init__.py
│   │   ├── postgres_repo.py
│   │   └── models.py
│   ├── pipeline/             # 데이터 파이프라인 관련 코드
│   │   ├── __init__.py
│   │   └── pipeline.py
│   ├── utils/                # 유틸리티 함수 및 클래스
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── app/                  # 웹 애플리케이션 코드
│       ├── __init__.py
│       ├── main.py
│       ├── components/
│       └── data/
├── tests/                    # 테스트 코드
│   ├── conftest.py
│   ├── test_download/
│   ├── test_preprocess/
│   ├── test_repository/
│   └── test_pipeline/
├── config/                   # 설정 파일
│   ├── config.yaml
│   └── db_config.yaml
├── scripts/                  # 스크립트
│   ├── run_pipeline.py
│   └── create_db.py
├── data/                     # 데이터 파일 (원본 CSV 및 처리된 데이터)
├── docs/                     # 문서
├── .gitignore
├── setup.py
├── requirements.txt
└── README.md
```

