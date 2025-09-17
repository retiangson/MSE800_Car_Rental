import pytest
from faker import Faker
from fastapi.testclient import TestClient
from api.main_api import app
from Contracts.Enums.StatusEnums import UserStatus

faker = Faker()

client = TestClient(app)

def test_register_and_get_user():
    integration_user = faker.user_name()
    payload = {
        "id": None,
        "username": integration_user,
        "password": "password123",
        "role": "customer",
        "name": "Integration Tester",
        "contact_number": "1234567890",
        "email": "test@example.com",
        "address": "123 Test Street",
        "status": UserStatus.ACTIVE
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == integration_user
    user_id = data["id"]

    # Fetch same user
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == integration_user
