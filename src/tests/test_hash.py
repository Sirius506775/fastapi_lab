import bcrypt

# bcrypt는 salt를 지원함
# salt 기능을 사용하면, 같은 비밀번호에 대해 다른 해시값을 생성할 수 있음
# 이는 같은 비밀번호를 사용하더라도, 다른 해시값을 생성하여, 보안성을 높일 수 있음
# 암호를 탈취하려는 레인보우 테이블 공격을 방지할 수 있음
# salt를 사용하지 않으면, 같은 비밀번호에 대해 항상 같은 해시값을 생성함


def test_hash_password():
    password = "password"
    byte_password = password.encode("utf-8")
    hash_1 = bcrypt.hashpw(byte_password, salt=bcrypt.gensalt())
    hash_2 = bcrypt.hashpw(byte_password, salt=bcrypt.gensalt())

    assert bcrypt.checkpw(byte_password, hash_1)
    assert bcrypt.checkpw(byte_password, hash_2)
