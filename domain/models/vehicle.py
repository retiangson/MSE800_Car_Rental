# Domain/Models/Vehicle.py
from sqlalchemy import Column, Integer, String, Float
from Domain.Repositories.DBManager import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vtype = Column(String, nullable=False)
    base_rate = Column(Float, nullable=False)
    status = Column(String, default="Active")   # Active, Deleted, Inactive
