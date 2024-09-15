from fastapi import APIRouter, Depends, HTTPException

from database.orm import User
from database.userRepository import UserRepository
from schema.request import LoginRequest, SignUpRequest
from schema.response import JWTResponse, UserSchema
from service.userService import UserService

router = APIRouter(prefix="/users", tags=["users"])


# TODO: 회원가입 API 구현
# 1. request body로 username, password를 받는다.
# (2) 중복된 사용자인지 확인한다. - 추후 추가가 필요한 부분
# 2. password를 hash화 한다.
# 3. User 객체를 생성한다.
# 4. User 객체를 DB에 저장한다.
# 5. 저장된 User 객체를 반환한다.


# 추후 중복된 사용자인지 확인해야함 ...!
@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest, user_service: UserService = Depends(), user_repo: UserRepository = Depends()
):

    hashed_password: str = user_service.hash_password(plain_password=request.password)

    user: User = User.create(username=request.username, hashed_password=hashed_password)
    user: User = user_repo.save_user(user=user)  # user_id가 int로 실제 저장되는 시점

    return UserSchema.from_orm(user)


# TODO: 로그인 API 구현
# -[x] 1. request body로 username, password를 받는다.
# -[x] 2. 데이터베이스에서 username으로 User 객체를 찾는다.
# -[x]3. User 객체의 password(hashed)와 request로 받은 password가 같은지 비교한다. -> bcrypt.checkpw()
# -[x] 3.1 유효한 User인 경우 , JWT 토큰을 발급하여, 반환한다.
# -[] 3.2 유효하지 않은 User인 경우, 에러를 반환한다.


@router.post("/log-in", status_code=200)
def user_log_in_handler(
    request: LoginRequest, user_service: UserService = Depends(), user_repo: UserRepository = Depends()
):

    user: User | None = user_repo.get_user_by_username(username=request.username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verified: bool = user_service.verify_password(plain_password=request.password, hashed_password=user.password)
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")

    access_token: str = user_service.create_jwt(username=user.username)

    return JWTResponse(access_token=access_token)
