# Domain/Models/Car.py
from typing import List
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, Float, Enum
from Domain.Repositories.DBManager import Base
from Contracts.Enums.StatusEnums import CarStatus


class Car(Base):
    """
    ORM model representing a car in the Car Rental System.

    Each car record represents a vehicle available for rent.
    Admin users can add, update, deactivate, or soft-delete cars.
    """

    __tablename__ = "cars"  # Database table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String, nullable=False)   # Manufacturer (e.g., Toyota)
    model = Column(String, nullable=False)  # Model (e.g., Corolla)
    year = Column(Integer, nullable=False)  # Year of manufacture
    vtype = Column(String, nullable=False)  # Vehicle type (sedan, suv, ev, etc.)
    base_rate = Column(Float, nullable=False)  # Daily base rental rate
    status = Column(Enum(CarStatus), default=CarStatus.AVAILABLE, nullable=False)

    #Bidirectional relationship with rentals
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="car")

    def __repr__(self):
        """String representation for debugging/logging."""
        return (
            f"<Car id={self.id}, make='{self.make}', model='{self.model}', "
            f"year={self.year}, vtype='{self.vtype}', rate={self.base_rate}, "
            f"status='{self.status.name if self.status else None}'>"
        )
