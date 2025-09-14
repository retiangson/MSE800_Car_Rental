# Domain/DTOs/CarDto.py
from dataclasses import dataclass

@dataclass
class CarDto:
    id: int | None
    make: str
    model: str
    year: int
    vtype: str
    base_rate: float
    status: str  # Active, Deleted, Inactive
