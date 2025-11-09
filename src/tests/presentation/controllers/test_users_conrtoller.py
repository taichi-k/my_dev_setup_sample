from fastapi.testclient import TestClient

from app.application.users.users_service import UsersService
from app.infra.repositories.mock_users_repository import MockUsersRepository
from app.main import app
from app.presentation.controllers.users_deps import get_users_service

mock_repo = MockUsersRepository()


def override_users_service() -> UsersService:
    return UsersService(mock_repo)


app.dependency_overrides[get_users_service] = override_users_service

client = TestClient(app)


def test_users_create_path_returns_200() -> None:
    new_user_data = {"username": "new", "age": 25, "email": "new@example.com"}
    res = client.post("/user/create", json=new_user_data)
    assert res.status_code == 200
    assert res.json().get("result") == "ok"


def test_users_create_path_invalid_data() -> None:
    invalid_user_data = {"username": "", "age": -5, "email": "invalid-email"}
    res = client.post("/user/create", json=invalid_user_data)
    assert res.status_code == 422  # Unprocessable Entity for validation errors


def test_users_get_path_returns_200() -> None:
    username = "default"
    res = client.get(f"/user/{username}")
    assert res.status_code == 200
