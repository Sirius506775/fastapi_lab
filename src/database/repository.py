# repository pattern을 통해 데이터를 관리하는 코드를 명시적으로 분리하여 작성

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import Todo


def get_todos(session: Session) -> List[Todo]:
    return list(session.scalars(select(Todo)))


def get_todo_by_id(
    session: Session, todo_id: int
) -> Todo | None:  # Todo 객체를 반환하거나, None을 반환 3.10부터 가능(아래 버젼은 Optional[Todo]로 사용)
    return session.scalar(select(Todo).where(Todo.id == todo_id))


def create_todo(session: Session, todo: Todo) -> Todo:
    session.add(todo)  # session에 todo 인스턴스 추가
    session.commit()  # session에 추가된 todo 인스턴스를 DB에 반영(실제 저장되는 시점)
    session.refresh(instance=todo)  # db에 저장된 todo 인스턴스를 다시 읽어옴(이 시점에 todo id가 생성됨)
    return todo  # 생성된 todo 인스턴스 반환


def update_todo(session: Session, todo: Todo) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(instance=todo)
    return todo


def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(delete(Todo).where(Todo.id == todo_id))
    session.commit()
