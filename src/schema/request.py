from pydantic import BaseModel

# pydantic을 사용하여 request를 모델링


class CreateTodoRequest(BaseModel):
    contents: str
    is_done: bool


class SignUpRequest(BaseModel):
    username: str
    password: str
