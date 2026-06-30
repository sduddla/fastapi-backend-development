import re

from pydantic import BaseModel, EmailStr, Field, field_validator

# 할 일 생성 요청 모델
class TodoCreateRequest(BaseModel): # 생성 요청 모델 이름 정의
    # 요청 본문 필드 구성
    title: str
    is_done: bool = False

# 할 일 수정 요청 모델
class TodoUpdateRequest(BaseModel): # 수정 요청 모델 이름 정의
    title: str | None = None
    is_done: bool | None = None

# 회원가입 요청 모델
class UserSignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 주소") # 이메일 형식 검증
    password: str = Field(..., min_length=8, description="사용자 비밀번호(평문 입력)") # 비밀번호 규칙 검증

    @field_validator("password") # 비밀번호 필드 검증 데코레이터
    @classmethod
    def validate_password(cls, value): # 비밀번호 검증 함수
        if not re.search(r"[A-Z]", value):
            raise ValueError("비밀번호에는 대문자가 최소 1개 포함되어야 합니다.")
        if not re.search(r"[a-z]", value):
            raise ValueError("비밀번호에는 소문자가 최소 1개 포함되어야 합니다.")
        if not re.search(r"[0-9]", value):
            raise ValueError("비밀번호에는 숫자가 최소 1개 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*()_+]", value):
            raise ValueError("비밀번호에는 특수문자가 최소 1개 포함되어야 합니다.")
        return value

# 로그인 요청 모델
class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일 주소")
    password: str = Field(..., min_length=8, description="사용자 비밀번호(평문 입력)")