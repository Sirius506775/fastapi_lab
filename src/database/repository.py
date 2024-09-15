# repository pattern을 통해 데이터를 관리하는 코드를 명시적으로 분리하여 작성

from typing import List

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import Todo
from database.connection import get_db


class TodoRepository:
    def __init__(
        self, session: Session = Depends(get_db)
    ):  # fastapi가 recursive call(재귀 호출)을 해서 get_db()에 걸려 있는 의존성도 주입됨
        self.session = session  # session을 self 속성에 저장

    def get_todos(self) -> List[Todo]:
        return list(self.scalars(select(Todo)))

    def get_todo_by_id(
        self, todo_id: int
    ) -> Todo | None:  # Todo 객체를 반환하거나, None을 반환 3.10부터 가능(아래 버젼은 Optional[Todo]로 사용)
        return self.scalar(select(Todo).where(Todo.id == todo_id))

    def create_todo(self, todo: Todo) -> Todo:
        self.add(todo)  # session에 todo 인스턴스 추가
        self.commit()  # session에 추가된 todo 인스턴스를 DB에 반영(실제 저장되는 시점)
        self.refresh(instance=todo)  # db에 저장된 todo 인스턴스를 다시 읽어옴(이 시점에 todo id가 생성됨)
        return todo  # 생성된 todo 인스턴스 반환

    def update_todo(self, todo: Todo) -> Todo:
        self.add(todo)
        self.commit()
        self.refresh(instance=todo)
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.execute(delete(Todo).where(Todo.id == todo_id))
        self.commit()
