import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv() # .env 파일의 환경변수 로드

# 토큰 서명에 사용할 비밀키 설정
SECRET_KEY = os.environ["SECRET_KEY"]
# 서명 알고리즘 지정
ALGORITHM = "HS256"

# 엑세스 토큰 생성1
def create_access_token(user_id: int, expires_minutes: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }

    # 토큰 생성 및 반환
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# 엑세스 토큰 검증  및 사용자 정보 추출
def decode_access_token(token: str) -> int:
    try:
        # 토큰 디코딩 및 사용자 아이디 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    # 유효하지 않은 토큰 예외 처리
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )