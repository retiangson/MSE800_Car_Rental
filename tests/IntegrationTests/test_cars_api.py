import pytest
from fastapi.testclient import TestClient
from api.main_api import app
from Domain.Repositories.DBManager import Base, engine, init_db
from Contracts.Enums.StatusEnums import CarStatus

@pytest.fixture(autouse=True, scope="function")
def setup_db():
    """Recreate all tables before each API test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()  # if you have seed logic, otherwise just create_all is enough

@pytest.fixture
def client(setup_db):
    """Provide a TestClient with fresh DB schema."""
    return TestClient(app)


def test_add_and_list_cars(client):
    payload = {
        "id": None,
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021,
        "vtype": "sedan",
        "base_rate": 60.0,
        "status": CarStatus.AVAILABLE.value,
    }
    response = client.post("/cars/", json=payload)
    assert response.status_code == 200
    car = response.json()
    assert car["make"] == "Toyota"
    assert car["status"] == CarStatus.AVAILABLE.value

    # List cars
    list_resp = client.get("/cars/")
    assert list_resp.status_code == 200
    cars = list_resp.json()
    assert any(
        c["make"] == "Toyota" and c["status"] == CarStatus.AVAILABLE.value
        for c in cars
    )


def test_delete_and_restore_car(client):
    payload = {
        "id": None,
        "make": "Honda",
        "model": "Civic",
        "year": 2022,
        "vtype": "sedan",
        "base_rate": 70.0,
        "status": CarStatus.AVAILABLE.value,
    }
    response = client.post("/cars/", json=payload)
    car_id = response.json()["id"]

    # Delete
    del_resp = client.delete(f"/cars/{car_id}")
    assert del_resp.status_code == 200

    # Restore
    restore_resp = client.put(f"/cars/{car_id}/restore")
    assert restore_resp.status_code == 200

    # Verify restored car with normal GET (no ?include_deleted)
    get_resp = client.get(f"/cars/{car_id}")
    assert get_resp.status_code == 200
    restored_car = get_resp.json()
    assert restored_car["status"] == CarStatus.AVAILABLE.value
