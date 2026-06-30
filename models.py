from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func # 칼럼 타입 임포트
from sqlalchemy.orm import Mapped, mapped_column, relationship # ORM 칼럼 매핑 도구 임포트
from database.orm import Base # ORM 기준 클래스 임포트

# Todo 모델 정의
class Todo(Base):
    __tablename__ = "todo" # 테이블 이름 지정

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    user_id: Mapped[int | None] = mapped_column( # 외래키 설정
        ForeignKey("user.id"),
        nullable=True,
    )
    user: Mapped["User"] = relationship( # ORM 객체 관계 설정(Todo -> User)
        back_populates="todos",
    )

# User 모델 정의
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True) # 사용자 기본 식별자
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column( # 사용자 비밀번호(해시된 값)
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column( # 계정 생성 시작
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    todos: Mapped[list["Todo"]] = relationship( # ORM 객체 관계 설정(User -> Todo)
        back_populates="user",
        cascade="all, delete-orphan",
    )