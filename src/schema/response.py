from typing import List
from pydantic import BaseModel


# reseponse을 한 번 더 분리하고 정의해야하는 이유는 칼럼 간의 연산이나, 객체를 중첩 구조로 반환하는 경우, 특정 필드 값을 제외하고 리턴하는 경우 등 다양한 usecase에 대응하기 위함
# pydantic에서 sqlalchmey를 사용할 때, orm model을 사용하지 않고, pydantic의 BaseModel을 사용하여 schema를 정의하고, 이를 통해 데이터를 serialize하거나 deserialize할 수 있음


class TodoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    # entityToDto
    class Config:
        orm_mode = True  # sqlalchemy을 통해 매핑하여 가져온 Todo 모델을 pydantic의 모델로 변환할 때 사용 -> pydantic에서 sqlalchemey를 바로 읽어줄 수 있게 하기 위함


# response dto
class TodoListSchema(BaseModel):  # 실제로 응답에 사용할 클래스
    todos: List[TodoSchema]  # 전체 todo 리스트를 담을 리스트


class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class JWTResponse(BaseModel):
    access_token: str
    # token_type: str
    # user: UserSchema
