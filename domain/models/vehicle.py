
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Abstract base class demonstrating encapsulation and abstraction."""
    def __init__(self, make: str, model: str, year: int, base_rate: float, vtype: str):
        self._make = make
        self._model = model
        self._year = year
        self._base_rate = base_rate
        self._type = vtype

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model

    @property
    def year(self) -> int:
        return self._year

    @property
    def base_rate(self) -> float:
        return self._base_rate

    @property
    def vehicle_type(self) -> str:
        return self._type

    @abstractmethod
    def description(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model} ({self.vehicle_type})"
