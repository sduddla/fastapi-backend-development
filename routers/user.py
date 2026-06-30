from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from schema.request import UserSignUpRequest, UserLoginRequest
from database.db_connection import SessionFactory
from models import User
from auth.password import hash_password, verify_password
from schema.response import UserSignUpResponse
from fastapi import Request
from auth.token import create_access_token

router = APIRouter(tags=["User"])

# 회원가입
@router.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSignUpResponse, # 응답 모델 지정
)
def signup_user_handler(body: UserSignUpRequest): # 요청 데이터 검증
    # 이메일 중복 검사
    with SessionFactory() as session: # 데이터베이스 세션 생성
        stmt = select(User).where(User.email == body.email) # 이메일 중복 조회 쿼리 객체 생성
        existing_user = session.scalar(stmt) # 쿼리 실행 및 결과 확인
        if existing_user: # 중복 이메일인 경우 오류 응답 반환
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다."
            )

        # 비밀번호 해시 생성
        hashed_password =hash_password(body.password)

        # User 모델 생성 후 DB 저장
        user = User( # User 모델 객체 생성
            email=str(body.email),
            hashed_password=hashed_password,
        )
        session.add(user) # DB 저장
        session.commit()

        session.refresh(user) # DB에서 생성된 값(id, created_at) 반영
        return user # 회원가입 결과 반환

# 로그인 (세션 방식)
# @router.post(
#     "/users/login",
#     status_code=status.HTTP_200_OK
# )
# def login_user_handler(request: Request, body: UserLoginRequest): # 매개변수 수정
#     # 사용자 조회
#     with SessionFactory() as session:
#         stmt = select(User).where(User.email == body.email)
#         user = session.scalar(stmt)
#
#         # 사용자 존재 여부 검증
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="이메일 또는 비밀번호가 올바르지 않습니다."
#             )
#
#         # 비밀번호 검증
#         if not verify_password(body.password, user.hashed_password):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="이메일 또는 비밀번호가 올바르지 않습니다."
#             )
#     # 로그인 성공 후 세션에 사용자 아이디 지정
#     request.session["user_id"] = user.id
#     return {"message": "로그인 성공"}

# 로그인 (JWT 방식)
@router.post("/users/login", status_code=status.HTTP_200_OK)
def login_user_handler(body: UserLoginRequest):
    # 사용자 조회
    with SessionFactory() as session:
        stmt = select(User).where(User.email == body.email)
        user = session.scalar(stmt)
        # 사용자 존재 여부 검증
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.")
        # 비밀번호 검증
        if not verify_password(body.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )
    # 사용자 인증 성공 후 토큰 생성
    access_token = create_access_token(user_id=user.id, expires_minutes=60)
    # 엑세스 토큰 반환
    return {"access_token": access_token}

# 로그아웃
@router.post(
    "/users/logout",
    status_code=status.HTTP_200_OK
)
def logout_user_handler(request: Request):
    request.session.clear()
    return {"message": "로그아웃 완료"}