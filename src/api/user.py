from fastapi import APIRouter, Depends

from database.orm import User
from database.userRepository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


# 추후 중복된 사용자인지 확인해야함 ...!
@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest, user_service: UserService = Depends(), user_repo: UserRepository = Depends()
):

    hashed_password: str = user_service.hash_password(plain_password=request.password)

    user: User = User.create(username=request.username, hashed_password=hashed_password)
    user: User = user_repo.save_user(user=user)  # user_id가 int로 실제 저장되는 시점

    return UserSchema.from_orm(user)
