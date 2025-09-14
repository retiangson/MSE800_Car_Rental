# Domain/Models/User.py
from sqlalchemy import Column, Integer, String
from Domain.Repositories.DBManager import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)   # hashed password
    role = Column(String, nullable=False, default="customer")  # customer or admin
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    status = Column(String, default="Active")   # Active, Deleted, Inactive
