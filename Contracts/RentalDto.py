from dataclasses import dataclass

@dataclass
class RentalDto:
    id: int | None
    car_id: int
    user_id: int
    start_date: str   # stored as YYYY-MM-DD string for UI simplicity
    end_date: str
    total_cost: float | None
    status: str       # Pending, Active, Completed, Cancelled, Deleted
