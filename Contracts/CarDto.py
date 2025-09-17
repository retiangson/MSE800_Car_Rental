from dataclasses import dataclass

@dataclass
class CarDto:
    """Data Transfer Object for Car entity."""

    id: int | None        # Unique identifier (None for new cars not yet saved)
    make: str             # Manufacturer (e.g., Toyota)
    model: str            # Model name (e.g., Corolla)
    year: int             # Year of manufacture
    vtype: str            # Vehicle type (sedan, SUV, EV, etc.)
    base_rate: float      # Daily rental base rate
    status: str           # Lifecycle status (Active, Deleted, Inactive)
