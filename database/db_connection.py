import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv() # .env 파일의 환경변수 로드

# 1. 데이터베이스 연결 정보 설정
DATABASE_URL = os.environ["DATABASE_URL"]

# 2. 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 3. 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)