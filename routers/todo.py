from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from starlette import status
from database.db_connection import get_session
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.token import decode_access_token

router = APIRouter(tags=["Todo"])
bearer = HTTPBearer(auto_error=False) # Bearer 인증 스키마 생성

# 전체 할 일 조회
@router.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK,
)
def get_todos_handler(
        session = Depends(get_session),
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    # 토큰 존재 여부 확인 및 사용자 식별
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.user_id == user_id)
    todos = session.execute(stmt).scalars().all() # 쿼리 실행 및 결과 변환
    return todos
    # finally:
        # session.close()

# 단일 할 일 조회
@router.get( # 경로 변수 사용하는 GET API 정의
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
def get_todo_handler(
        todo_id: int,
        session = Depends(get_session),
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.execute(stmt).scalars().first() # 쿼리 실행 및 단일 결과 선택
    if todo: # 결과 반환
        return todo
    raise HTTPException( # 조회 실패 시 예외 처리
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
    )
    # finally:
        # session.close()

# 할 일 생성
@router.post( # POST API 정의
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_todo_handler(
        body: TodoCreateRequest,
        session = Depends(get_session),
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    # session = SessionFactory()
    # try:
    todo = Todo( # ORM 모델 객체 생성
        title=body.title,
        is_done=body.is_done,
        user_id=user_id,
    )
    session.add(todo) # 세션에 등록
    session.commit() # 데이터베이스에 저장
    return todo # 생성 결과 반환
    # finally:
        # session.close()

# 할 일 수정
@router.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
def update_todo_handler(
        todo_id: int,
        body: TodoUpdateRequest,
        session = Depends(get_session),
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.execute(stmt).scalars().first() # 쿼리 실행 및 단일 결과 선택
    if todo:
        if body.title is not None: # 제목 수정
            todo.title = body.title
        if body.is_done is not None: # 완료 여부 수정
            todo.is_done = body.is_done
        session.commit() # 변경 사항 저장
        return todo # 수정 결과 반환
    raise HTTPException( # 조회 실패 시 예외 처리
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )
    # finally:
        # session.close()

# 할 일 삭제
@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo_handler(
        todo_id: int,
        session = Depends(get_session),
        authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    # session = SessionFactory()
    # try:
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.execute(stmt).scalars().first() # 쿼리 실행 및 단일 결과 선택
    if todo: # 조회 결과 확인
        session.delete(todo) # 삭제 대상으로 지정
        session.commit() # 변경 사항 저장
        return # 응답 반환(본문 없음)
    raise HTTPException( # 조회 실패 시 예외 처리
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )
    # finally:
        # session.close()
