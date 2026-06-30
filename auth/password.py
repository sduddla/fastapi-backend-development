from pwdlib import PasswordHash

# 비밀번호 해싱 설정 객체 설정
password_hasher = PasswordHash.recommended()

# 평문 비밀번호 -> 해시 문자열 반환
def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)

# 평문 비밀번호와 해시값 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)