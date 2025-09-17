# Domain/Models/Car.py
from sqlalchemy import Column, Integer, String, Float
from Domain.Repositories.DBManager import Base

class Car(Base):
    """
    ORM model representing a car in the Car Rental System.

    Each car record represents a vehicle available for rent. 
    Admin users can add, update, deactivate, or soft-delete cars.

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier.
        make (str): Manufacturer of the car (e.g., "Toyota").
        model (str): Specific car model (e.g., "Corolla").
        year (int): Year of manufacture.
        vtype (str): Vehicle type (e.g., "sedan", "SUV", "EV").
        base_rate (float): Base daily rental rate (before discounts/fees).
        status (str): Current status of the car ("Active", "Deleted", "Inactive").
    """
    __tablename__ = "cars" # Database table name

    id = Column(Integer, primary_key=True, autoincrement=True) 
    make = Column(String, nullable=False)  # Car manufacturer e.g., Toyota
    model = Column(String, nullable=False) # Car model e.g., Corolla
    year = Column(Integer, nullable=False) # Production year
    vtype = Column(String, nullable=False)   # Vehicle type/category eg. sedan, suv, ev, etc.
    base_rate = Column(Float, nullable=False) # Base rental price per day
    status = Column(String, default="Active")   # Active, Deleted, Inactive

    def __repr__(self):
        """
        String representation for debugging/logging.
        Example:
            <Car id=1, make='Toyota', model='Corolla', year=2020, vtype='sedan', rate=50.0, status='Active'>
        """
        return f"<Car id={self.id}, make='{self.make}', model='{self.model}', year={self.year}, vtype='{self.vtype}', rate={self.base_rate}, status='{self.status}'>"