import pytest
from fastapi.testclient import TestClient
from main import app


# 데코레이터를 추가하여 pytest가 client() 함수를 fixture로 인식하도록 한다.
# 테스트코드 안에서 global로 선언된 client 객체를 사용할 수 있게 된다.
@pytest.fixture
def client():
    return TestClient(app=app)
