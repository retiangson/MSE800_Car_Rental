from fastapi import APIRouter, HTTPException
from typing import List
from Contracts.RentalDto import RentalDto
from Business.Services.RentalService import RentalService
from datetime import datetime

router = APIRouter(prefix="/rentals", tags=["Rentals"])
rental_service: RentalService = None  # Injected later in main_api

@router.get("/", response_model=List[RentalDto])
def list_rentals(include_deleted: bool = False):
    """Get all rentals (optionally include deleted)."""
    return rental_service.list_rentals(include_deleted=include_deleted)

@router.get("/active", response_model=List[RentalDto])
def list_active_rentals():
    """Get all rentals currently marked as Active."""
    return rental_service.list_active_rentals()

@router.post("/", response_model=RentalDto)
def create_rental(rental: RentalDto):
    """Create a new rental request."""
    saved = rental_service.create_rental(rental)
    if not saved:
        raise HTTPException(status_code=400, detail="Failed to create rental")
    return saved

@router.put("/{rental_id}/approve")
def approve_rental(rental_id: int):
    """Approve and start a rental request."""
    if not rental_service.approve_and_start_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found or invalid")
    return {"message": "Rental approved and started"}

@router.put("/{rental_id}/complete")
def complete_rental(rental_id: int, actual_return: str):
    """Complete a rental and calculate final cost using return date (YYYY-MM-DD)."""
    try:
        return_date = datetime.strptime(actual_return, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")

    if not rental_service.complete_rental(rental_id, return_date):
        raise HTTPException(status_code=404, detail="Rental not found or invalid")
    return {"message": "Rental completed successfully"}

@router.put("/{rental_id}/cancel")
def cancel_rental(rental_id: int):
    """Cancel a rental request."""
    if not rental_service.cancel_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found")
    return {"message": "Rental cancelled successfully"}

@router.delete("/{rental_id}")
def delete_rental(rental_id: int):
    """Soft delete a rental (mark as Deleted)."""
    if not rental_service.delete_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found")
    return {"message": "Rental deleted successfully"}
