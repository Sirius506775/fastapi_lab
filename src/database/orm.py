from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateTodoRequest

Base = declarative_base()  # ORM을 사용하기 위한 Base 클래스 생성


class Todo(Base):
    __tablename__ = "todo"  # todos 테이블 생성(없으면 생성, 있으면 사용)

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):  # 어떤 Todo 객체인지 확인하기 위해, __repr__ 메서드를 오버라이딩하여 사용
        return f"Todo: {self.id}, {self.contents}, {self.is_done}"

    @classmethod  # pydantic 객체를 ORM 객체로 변환하는 클래스 메소드 정의 - dtoToEntity
    def create(cls, request: CreateTodoRequest) -> "Todo":
        return cls(contents=request.contents, is_done=request.is_done)

    # 유지보수성을 위해 Todo 객체의 상태를 변경하는 메소드를 인스턴스 메소드로 정의
    def done(self) -> "Todo":
        self.is_done = True
        # 객체의 상태가 변경되었을 때, 특정 메소드를 여기서 호출하여, 바깥에서 파편화되지 않도록 할 수 있음
        return self

    def undone(self) -> "Todo":
        self.is_done = False
        return self


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship(
        "Todo", lazy="joined"
    )  # User와 Todo의 관계를 설정하여, User 객체로 Todo 객체에 접근할 수 있도록 함(객체참조)

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(username=username, password=hashed_password)
