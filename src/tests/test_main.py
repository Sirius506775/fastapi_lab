# 언더바 네이밍 컨벤션을 맞춰야 pytest가 파일을 찾아서 테스트를 실행할 수 있음
from database.orm import Todo
from database.repository import TodoRepository


def test_health_check(client):
    response = client.get("/")  # health_check_handler() 함수 실행
    assert response.status_code == 200  # HTTP 상태 코드가 200인지 확인
    assert response.json() == {"ping": "pong"}  # JSON response가 {"ping": "pong"}인지 확인


def test_get_todos(client, mocker):
    # order = asc
    mocker.patch.object(
        TodoRepository,
        "get_todos",
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


def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_id",
        return_value=Todo(id=1, contents="FastAPI Section 0", is_done=True),
    )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "FastAPI Section 0", "is_done": True}

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)
    response = client.get("/todos/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(client, mocker):
    # 201
    create_spy = mocker.spy(
        Todo, "create"
    )  # Todo.create() 메서드를 spy한다. -> spy 특정 객체를 tracking하고, 그 개체가 어떤 반환값이나 연산을 했었는데 객체 안에 저장

    mocker.patch.object(
        TodoRepository,
        "create_todo",
        return_value=Todo(id=1, contents="FastAPI Section 0", is_done=True),
    )

    body = {"contents": "test", "is_done": False}

    response = client.post("/todos", json=body)

    # spy 객체의 반환값을 확인
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done == False

    # response 확인
    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "FastAPI Section 0", "is_done": True}


def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_id",
        return_value=Todo(id=1, contents="FastAPI Section 0", is_done=True),
    )
    undone = mocker.patch.object(Todo, "undone")
    mocker.patch.object(
        TodoRepository,
        "update_todo",
        return_value=Todo(id=1, contents="FastAPI Section 0", is_done=False),
    )

    response = client.patch(
        "/todos/1", json={"is_done": False}
    )  # is_done이 False일 때, undone 메서드가 호출 / is_done이 True일 때, done 메서드가 호출

    undone.assert_called_once_with()  # undone 메서드가 한 번 호출되었는지 확인

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "FastAPI Section 0", "is_done": False}

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)
    response = client.patch("/todos/2", json={"is_done": False})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
        TodoRepository, "get_todo_by_id", return_value=Todo(id=1, contents="FastAPI Section 0", is_done=True)
    )
    mocker.patch.object(TodoRepository, "delete_todo", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)
    response = client.delete("/todos/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
