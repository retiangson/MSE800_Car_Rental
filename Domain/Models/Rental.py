# Domain/Models/Rental.py
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Domain.Repositories.DBManager import Base
from Contracts.Enums.StatusEnums import RentalStatus
from Domain.Models.User import User
from Domain.Models.Car import Car


class Rental(Base):
    """
    ORM model representing a rental transaction in the Car Rental System.

    A Rental record links a User (customer) with a Car over a specific date range.
    It stores the rental cost and current rental status.
    """

    __tablename__ = "rentals"  # Database table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who rented
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)  # Which car was rented
    start_date = Column(String, nullable=False)  # Rental start date (YYYY-MM-DD)
    end_date = Column(String, nullable=False)  # Rental end date (YYYY-MM-DD)
    total_cost = Column(Float, default=0.0)  # Total cost of the rental
    status = Column(Enum(RentalStatus), default=RentalStatus.PENDING, nullable=False)

    # Relationships
    user = relationship(User, back_populates="rentals")
    car = relationship(Car, back_populates="rentals")

    def __repr__(self):
        """String representation for debugging/logging."""
        return (
            f"<Rental id={self.id}, user_id={self.user_id}, car_id={self.car_id}, "
            f"status='{self.status.name if self.status else None}', cost={self.total_cost}>"
        )
