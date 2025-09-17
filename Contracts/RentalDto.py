from dataclasses import dataclass

@dataclass
class RentalDto:
    """Data Transfer Object for Rental entity."""

    id: int | None            # Unique identifier (None if not yet saved)
    car_id: int               # Foreign key → Car being rented
    user_id: int              # Foreign key → User (customer renting)
    start_date: str           # Rental start date (YYYY-MM-DD format)
    end_date: str             # Rental end date (YYYY-MM-DD format)
    total_cost: float | None  # Calculated cost of the rental (None until set)
    status: str               # Lifecycle status (Pending, Active, Completed, Cancelled, Deleted)
