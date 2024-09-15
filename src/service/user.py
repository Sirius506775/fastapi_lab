import bcrypt


class UserService:
    encoding: str = "utf-8"

    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)
