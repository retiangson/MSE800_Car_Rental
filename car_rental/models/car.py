
from .vehicle import Vehicle

class Car(Vehicle):
    """Concrete class demonstrating inheritance and polymorphism (description override)."""
    def description(self) -> str:
        return f"Car: {self.year} {self.make} {self.model} — type={self.vehicle_type}, base_rate={self.base_rate}"
