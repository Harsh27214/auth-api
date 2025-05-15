import pytest
from fastapi.testclient import TestClient
from routes import app
from database import SessionFactory
from models import User

@pytest.fixture
def session():
    with SessionFactory() as test_session:
        test_session.query(User).delete()
        test_session.commit()
        return test_session

@pytest.fixture
def client():
    return TestClient(app)

class TestCreateUser:
    valid_username = "John"
    strong_password = "@Password1"

    def test_create_user_success(self, client, session):
        response = client.post("/users", json={"username": self.valid_username, "password": self.strong_password})
        assert response.status_code == 201
        assert response.json() == {"message": "User created", "username": self.valid_username}

    def test_create_user_existing_username(self, client, session):
        client.post("/users", json={"username": self.valid_username, "password": self.strong_password})
        response = client.post("/users", json={"username": self.valid_username, "password": "@DifferentStrongPassword1"})
        assert response.status_code == 409
        assert response.json() == {"detail": "Username already exists"}

    def test_create_user_invalid_username(self, client, session):
        response = client.post("/users", json={"username": "Bo", "password": self.strong_password})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "Value error, Username must be 3 to 20 characters long"

    def test_create_user_weak_password(self, client, session):
        response = client.post("/users", json={"username": self.valid_username, "password": "WeakPassword"})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == "Value error, Password must contain more than seven characters with at least one lowercase letter, uppercase letter, digit, and special symbol"

    def test_create_user_missing_username(self, client, session):
        response = client.post("/users", json={"password": self.strong_password})
        assert response.status_code == 422

        data = response.json()
        error = data["detail"][0]
        assert error.get("type") == "missing"
        assert error.get("loc") == ["body", "username"]
        assert error.get("msg") == "Field required"

    def test_create_user_missing_password(self, client, session):
        response = client.post("/users", json={"username": self.valid_username})
        assert response.status_code == 422

        data = response.json()
        error = data["detail"][0]
        assert error.get("type") == "missing"
        assert error.get("loc") == ["body", "password"]
        assert error.get("msg") == "Field required"
