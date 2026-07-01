from fastapi import HTTPException, APIRouter, Depends, UploadFile, File
from sqlalchemy import select
from starlette import status
from database.db_connection import get_session
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse
from auth.dependencies import get_current_user_id
from pathlib import Path
import shutil
from fastapi.responses import FileResponse

router = APIRouter(tags=["Todo"])
UPLOAD_DIR = Path("uploads") # 파일을 저장할 폴더 경로 생성

# 전체 할 일 조회
@router.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK,
)
def get_todos_handler(
        session = Depends(get_session),
        user_id: int | None = Depends(get_current_user_id)
):
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
        user_id: int | None = Depends(get_current_user_id)
):
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
        user_id: int | None = Depends(get_current_user_id)
):
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
        user_id: int | None = Depends(get_current_user_id)
):
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
        user_id: int | None = Depends(get_current_user_id)
):
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

# 파일 업로드
@router.post("/upload")
def upload_file(file: UploadFile = File(...)): # 업로드 파일을 매개변수로 선언
    if not file.filename: # 파일 이름 없으면 거부
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="파일 이름이 없습니다."
        )
    UPLOAD_DIR.mkdir(exist_ok=True) # 업로드할 폴더 준비
    file_path = UPLOAD_DIR / file.filename # 저장할 파일 경로 생성
    with file_path.open("wb") as buffer: # 업로드된 파일 내용을 디스크에 저장
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename} # 업로드 결과 반환

# 파일 다운로드
@router.get("/files/{filename}")
def download_file(filename: str):
    file_path = UPLOAD_DIR / filename # 다운로드할 파일 경로 생성
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )