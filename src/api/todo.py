from typing import List
from fastapi import Body, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import TodoRepository
from database.orm import Todo, User

from database.userRepository import UserRepository
from middleware.security import get_access_token
from schema.response import TodoSchema, TodoListSchema
from schema.request import CreateTodoRequest
from service.userService import UserService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", status_code=200)
def get_todos_handler(
    access_token: str = Depends(get_access_token),  # get_access_token 함수를 통해 token을 받아온다.
    order: str | None = None,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    todo_repo: TodoRepository = Depends(),
) -> TodoListSchema:
    # access_token을 decode하여 username을 받아온다.
    username: str = user_service.decode_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    todos: List[Todo] = user.todos  # user.todos로 user가 가지고 있는 todo들을 가져온다.
    if order and order == "desc":
        return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]])
    return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos])  # list comprehension을 사용
    # todos를 순회하면서 todo 하나를 from_orm으로 전달하여 TodoSchema로 변환한 뒤, 만들어진 객체들을 리스트에 담아 반환한다.


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, todo_repo: TodoRepository = Depends()) -> TodoSchema:

    todo: Todo | None = todo_repo.get_todo_by_id(todo_id=todo_id)

    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("", status_code=201)  # 201: Created
def create_todo_handler(
    request: CreateTodoRequest, todo_repo: TodoRepository = Depends()
) -> TodoSchema:  # request가 CreateTodoRequest이라고 명시해주면 FastAPI가 자동으로 request body를 파싱해준다.

    todo = Todo.create(request=request)  # ORM 객체 생성(id=None)
    todo = todo_repo.create_todo(todo)  # ORM 객체를 DB에 저장(id=int)

    return TodoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int, is_done: bool = Body(..., embed=True), todo_repo: TodoRepository = Depends()
):  # Body를 사용해서 is_done 하나의 컬럼값을 받아올 수 있다.

    todo: Todo | None = todo_repo.get_todo_by_id(todo_id=todo_id)  # todo가 존재하는지 확인

    if todo:
        todo.done() if is_done else todo.undone()
        todo: Todo = todo_repo.update_todo(todo=todo)
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, todo_repo: TodoRepository = Depends()):

    todo: Todo | None = todo_repo.get_todo_by_id(todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_repo.delete_todo(todo_id=todo_id)
