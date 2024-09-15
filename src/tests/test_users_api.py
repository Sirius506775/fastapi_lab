from database.orm import User
from database.userRepository import UserRepository
from service.user import UserService


def test_user_sign_up(client, mocker):
    """유저 회원가입 테스트
    hasing을 하는 과정은 salt로 인해 랜덤성 동작을 하기 때문에 일정하게 검증하기 어려움
    어떤 개별 메소드에 대해 동작을 검증하는 유닛 테스트라는 별도의 테스트가 필요함
    하지만 여기서는 해싱이 정상적으로 동작한다고 가정하고, api flow에 대한 테스트만 진행합니다.
    """

    hash_password = mocker.patch.object(UserService, "hash_password", return_value="hashed")
    user_create = mocker.patch.object(User, "create", return_value=User(id=None, username="test", password="hashed"))

    mocker.patch.object(UserRepository, "save_user", return_value=User(id=1, username="test", password="hashed"))

    body = {"username": "test", "password": "plain"}

    response = client.post("/users/sign-up", json=body)

    hash_password.assert_called_once_with(  # 비밀번호 해싱 검증
        plain_password="plain"
    )  # router에서 plain_password가 request.password를 제대로 입력 받았는지 인자를 확인

    user_create.assert_called_once_with(  # User 객체 생성 검증
        username="test", hashed_password="hashed"
    )  # router에서 username과 hashed_password가 해쉬된 비밀번호 값을 제대로 입력 받았는지 인자를 확인

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "test"}  # 응답값 검증
