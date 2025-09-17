import pytest
from faker import Faker
from fastapi.testclient import TestClient
from api.main_api import app
from datetime import datetime, timedelta

faker = Faker()

from Contracts.Enums.StatusEnums import UserStatus, CarStatus 

client = TestClient(app)

def test_create_approve_and_complete_rental():
    # Add user
    rent_user = faker.user_name()
    user_payload = {
        "id": None,
        "username": rent_user,
        "password": "password123",
        "role": "customer",  
        "name": "Rental Tester",
        "contact_number": "9876543210",
        "email": "rent@example.com",
        "address": "456 Rent Street",
        "status": UserStatus.ACTIVE.value
    }
    user_resp = client.post("/users/", json=user_payload)
    assert user_resp.status_code == 200
    user_id = user_resp.json()["id"]

    # Add car
    car_payload = {
        "id": None,
        "make": "Ford",
        "model": "Focus",
        "year": 2020,
        "vtype": "sedan",
        "base_rate": 80.0,
        "status": CarStatus.AVAILABLE.value 
    }
    car_resp = client.post("/cars/", json=car_payload)
    assert car_resp.status_code == 200
    car_id = car_resp.json()["id"]

    # Create rental
    start_date = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")

    rental_payload = {
        "id": None,
        "car_id": car_id,
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_cost": None,
        "status": None
    }
    rental_resp = client.post("/rentals/", json=rental_payload)
    assert rental_resp.status_code == 200
    rental_id = rental_resp.json()["id"]

    # Approve rental
    approve_resp = client.put(f"/rentals/{rental_id}/approve")
    assert approve_resp.status_code == 200

    # Complete rental
    return_date = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    complete_resp = client.put(f"/rentals/{rental_id}/complete", params={"actual_return": return_date})
    assert complete_resp.status_code == 200
