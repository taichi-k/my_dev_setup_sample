from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_default() -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello from FastAPI on Dev Container!"}
