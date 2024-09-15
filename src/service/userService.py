from datetime import datetime, timedelta
import bcrypt
from jose import jwt


class UserService:
    encoding: str = "utf-8"
    secret_key: str = "3afa21d53830f04a26f81f54b8c06b135042971ff4278d3e1250893a0fada6c6"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # 추후 디테일한 try-except를 사용하여 예외처리를 추가해야함
        return bcrypt.checkpw(plain_password.encode(self.encoding), hashed_password.encode(self.encoding))

    # openssl rand -hex 32 명령어로 비밀키 생성하는 것을 선행
    def create_jwt(
        self,
        username: str,
    ) -> str:
        return jwt.encode(  # sub: subject, exp: expiration
            {"sub": username, "exp": datetime.now() + timedelta(days=1)},  # username은 추후 고유한 값으로 변경해야함
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(access_token, self.secret_key, algorithms=self.jwt_algorithm)

        # expire time을 확인하여, 만료된 토큰인지 확인하는 로직 추가 필요
        return payload["sub"]  # username
