# 언더바 네이밍 컨벤션을 맞춰야 pytest가 파일을 찾아서 테스트를 실행할 수 있음

from fastapi.testclient import TestClient

from database.orm import Todo


def test_health_check(client):
    response = client.get("/")  # health_check_handler() 함수 실행
    assert response.status_code == 200  # HTTP 상태 코드가 200인지 확인
    assert response.json() == {"ping": "pong"}  # JSON response가 {"ping": "pong"}인지 확인


def test_get_todos(client, mocker):
    # order = asc
    mocker.patch(
        "main.get_todos",
        return_value=[
            Todo(id=1, contents="FastAPI Section 0", is_done=True),
            Todo(id=2, contents="FastAPI Section 1", is_done=False),
        ],
    )
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
        ]
    }

    # order = desc
    response = client.get("/todos?order=desc")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }
