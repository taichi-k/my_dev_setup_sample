from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_users_create_path_returns_200():
    new_user_data = {"username": "new", "age": 25, "email": "new@example.com"}
    res = client.post("/user/create", json=new_user_data)
    assert res.status_code == 200
    assert res.json().get("result") == "ok"


def test_users_create_path_invalid_data():
    invalid_user_data = {"username": "", "age": -5, "email": "invalid-email"}
    res = client.post("/user/create", json=invalid_user_data)
    assert res.status_code == 422  # Unprocessable Entity for validation errors


def test_users_get_path_returns_200():
    username = "default"
    res = client.get(f"/user/{username}")
    assert res.status_code == 200
