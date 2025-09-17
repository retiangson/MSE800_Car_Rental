from fastapi import APIRouter, HTTPException, Body
from typing import List
from Contracts.CarDto import CarDto
from Business.Services.CarService import CarService

router = APIRouter(prefix="/cars", tags=["Cars"])
car_service: CarService = None  # Will be injected in main_api

@router.get("/", response_model=List[CarDto])
def list_cars(include_deleted: bool = False):
    """Get all cars (optionally include deleted ones)."""
    return car_service.list_cars(include_deleted=include_deleted)

@router.get("/available", response_model=List[CarDto])
def list_available_cars():
    """Get only cars that are available for rent."""
    return car_service.list_available_cars()

@router.post("/", response_model=CarDto)
def add_car(car: CarDto):
    """Add a new car to the system."""
    saved = car_service.add_car(car)
    if not saved:
        raise HTTPException(status_code=400, detail="Failed to add car")
    return saved

@router.put("/{car_id}", response_model=CarDto)
def update_car(car_id: int, dto: CarDto = Body(...)):
    """Update car details by ID."""
    dto.id = car_id
    updated = car_service.update_car(dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated

@router.delete("/{car_id}")
def delete_car(car_id: int):
    """Soft delete a car (mark as Deleted)."""
    if not car_service.delete_car(car_id):
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}

@router.put("/{car_id}/restore")
def restore_car(car_id: int):
    """Restore a previously deleted car."""
    if not car_service.restore_car(car_id):
        raise HTTPException(status_code=404, detail="Car not found or not deleted")
    return {"message": "Car restored successfully"}
