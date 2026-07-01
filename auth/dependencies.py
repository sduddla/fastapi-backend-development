from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.token import decode_access_token

bearer = HTTPBearer(auto_error=False) # Bearer 인증 스키마 생성

# 토큰에서 사용자 식별 (공통 의존성)
def get_current_user_id(
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
) -> int | None:
    if authorization: # 토큰 존재 여부 확인 및 사용자 식별
        return decode_access_token(authorization.credentials)
    return None