import os

from dotenv import load_dotenv
from fastapi import FastAPI
# from database.db_connection import engine # 데이터베이스 엔진 임포트
from database.db_connection import engine  # 세선 팩토리 임포트
from database.orm import Base # ORM 기준 클래스 임포트
from routers.todo import router as todo_router
from routers.user import router as user_router
from starlette.middleware.sessions import SessionMiddleware # 세션 미들웨어 임포트
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_):
    Base.metadata.create_all(bind=engine)
    yield

load_dotenv() # .env 파일의 환경변수 로드
app = FastAPI(lifespan=lifespan)
app.include_router(todo_router)
app.include_router(user_router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET_KEY"],
)