# Domain/Models/Rental.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Domain.Repositories.DBManager import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    total_cost = Column(Float, default=0.0)
    status = Column(String, default="Pending")   # Pending, Approved, Active, Completed, Cancelled, Deleted

    user = relationship("User")
    car = relationship("Car")
