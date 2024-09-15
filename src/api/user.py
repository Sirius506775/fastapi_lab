from fastapi import APIRouter, Depends, HTTPException

from database.orm import User
from database.userRepository import UserRepository
from middleware.security import get_access_token
from schema.request import CreateOTPRequest, LoginRequest, SignUpRequest, VerifyOTPRequest
from schema.response import JWTResponse, UserSchema
from service.userService import UserService

from util.cashe import redis_client

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


# -[x] 1. access_token을 받아서, 유효한지 확인(여기서는 회원가입 이후, 이메일 인증이기 때문에)
# -[x] 2. request body로 email을 받는다.
# -[x] 3. email로 otp를 생성한다.(randome 4 digit number)
# -[x] 4. redis에 otp를 저장한다.(email: 1234, exp=3min)
# -[] 5. email로 otp를 전송한다.


@router.post("/email/otp", status_code=200)
def create_opt_handler(
    request: CreateOTPRequest,
    _: str = Depends(get_access_token),  # header에서 검증만 하고, 사용하지 않을 경우 _로 처리
    user_service: UserService = Depends(),
):

    otp: int = user_service.create_otp()
    redis_client.set(request.email, otp)  # set 명령으로 key-value 저장
    redis_client.expire(request.email, 3 * 60)  # 만료시간 설정 3분

    # 여기에 이메일 전송 로직을 추가해야하나, 현재는 생략

    return {"otp": otp}


# -[x] 1. access_token 검증, 인증된 사용자만 요청 가능
# -[x] 2. request body로 email, otp를 받는다.
# -[x] 3. redis에서 email로 otp를 조회한다.(request로 받은 otp와 비교)
# -[] 4. otp가 일치하면, email 인증 성공


@router.post("/email/otp/verify", status_code=200)
def verify_opt_handler(
    request: VerifyOTPRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):
    otp: str | None = redis_client.get(
        request.email
    )  # 저장한 otp를 가져옴 - redis에서는 value를 string으로 저장하기 때문에, 형변환 필요
    if not otp:
        raise HTTPException(status_code=404, detail="Bad Request")

    if request.otp != int(otp):  # 검증할 때  int로 형변환
        raise HTTPException(status_code=404, detail="Bad Request")

    username: str = user_service.decode_jwt(access_token)
    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # save email to user
    # 추후 이메일 컬럼을 추가하여, 저장해야함

    return UserSchema.from_orm(user)
