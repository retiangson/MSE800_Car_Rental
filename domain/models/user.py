# Domain/Models/User.py
from sqlalchemy.orm import relationship, Mapped
from typing import List
from sqlalchemy import Column, Integer, String, Enum
from Domain.Repositories.DBManager import Base
from Contracts.Enums.StatusEnums import UserStatus


class User(Base):
    """
    ORM model representing a system user in the Car Rental System.

    This table stores both customers and admins.
    Roles determine access control (e.g., only admins can manage cars and rentals).
    """

    __tablename__ = "users"  # Database table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)  # Unique login username
    password = Column(String, nullable=False)  # Hashed password
    role = Column(String, nullable=False, default="customer")  # Role: "customer" or "admin"
    name = Column(String, nullable=False)  # Full name
    contact_number = Column(String, nullable=True)  # Optional
    email = Column(String, nullable=True)  # Optional
    address = Column(String, nullable=True)  # Optional
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    #Bidirectional relationship with rentals
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="user")

    def __repr__(self):
        """String representation for debugging/logging."""
        return (
            f"<User id={self.id}, username='{self.username}', "
            f"role='{self.role}', status='{self.status.name if self.status else None}'>"
        )
