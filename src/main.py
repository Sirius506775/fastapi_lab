from typing import List
from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import create_todo, delete_todo, get_todos, get_todo_by_id, update_todo
from database.orm import Todo

from schema.response import TodoSchema, TodoListSchema
from schema.request import CreateTodoRequest

# FastAPI 인스턴스 생성
app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.get("/todos", status_code=200)
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
) -> TodoListSchema:

    todos: List[Todo] = get_todos(session=session)

    if order and order == "desc":
        return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]])
    return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos])  # list comprehension을 사용
    # todos를 순회하면서 todo 하나를 from_orm으로 전달하여 TodoSchema로 변환한 뒤, 만들어진 객체들을 리스트에 담아 반환한다.


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, session: Session = Depends(get_db)) -> TodoSchema:

    todo: Todo | None = get_todo_by_id(session=session, todo_id=todo_id)

    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", status_code=201)  # 201: Created
def create_todo_handler(
    request: CreateTodoRequest, session: Session = Depends(get_db)
) -> TodoSchema:  # request가 CreateTodoRequest이라고 명시해주면 FastAPI가 자동으로 request body를 파싱해준다.

    todo = Todo.create(request=request)  # ORM 객체 생성(id=None)
    todo = create_todo(session, todo)  # ORM 객체를 DB에 저장(id=int)

    return TodoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int, is_done: bool = Body(..., embed=True), session: Session = Depends(get_db)
):  # Body를 사용해서 is_done 하나의 컬럼값을 받아올 수 있다.

    todo: Todo | None = get_todo_by_id(session=session, todo_id=todo_id)  # todo가 존재하는지 확인

    if todo:
        todo.done() if is_done else todo.undone()
        todo: Todo = update_todo(session=session, todo=todo)
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, session: Session = Depends(get_db)):

    todo: Todo | None = get_todo_by_id(session=session, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    delete_todo(session=session, todo_id=todo_id)