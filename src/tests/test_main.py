def test_health_check(client):
    response = client.get("/")  # health_check_handler() 함수 실행
    assert response.status_code == 200  # HTTP 상태 코드가 200인지 확인
    assert response.json() == {"ping": "pong"}  # JSON response가 {"ping": "pong"}인지 확인
