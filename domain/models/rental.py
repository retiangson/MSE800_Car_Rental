# Domain/Models/Rental.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from Domain.Repositories.DBManager import Base

class Rental(Base):
    """
    ORM model representing a rental transaction in the Car Rental System.

    A Rental record links a User (customer) with a Car over a specific date range.
    It stores the rental cost and current rental status.

    Attributes:
        id (int): Primary key, auto-incrementing rental identifier.
        user_id (int): Foreign key → users.id (the customer renting the car).
        car_id (int): Foreign key → cars.id (the rented car).
        start_date (str): Rental start date (stored as string for simplicity, format: YYYY-MM-DD).
        end_date (str): Rental end date (same format)
        total_cost (float): Calculated cost for the rental (base_rate x days + fees).
        status (str): Current state of the rental:
            - "Pending"   → awaiting admin approval
            - "Approved"  → approved but not yet active
            - "Active"    → currently ongoing
            - "Completed" → finished rental
            - "Cancelled" → cancelled by customer/admin
            - "Deleted"   → soft-deleted record
    """
        
    __tablename__ = "rentals" # Database table name
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Who rented
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False) # Which car was rented
    start_date = Column(String, nullable=False) # Rental start date
    end_date = Column(String, nullable=False) # Rental end date
    total_cost = Column(Float, default=0.0) # Total cost
    status = Column(String, default="Pending")   # Pending, Approved, Active, Completed, Cancelled, Deleted

    user = relationship("User")  # Link to User object
    car = relationship("Car") # Link to Car object

    def __repr__(self):
        """
        String representation for debugging/logging.
        Example:
            <Rental id=5, user_id=1, car_id=3, status='Active', cost=150.0>
        """
        return f"<Rental id={self.id}, user_id={self.user_id}, car_id={self.car_id}, status='{self.status}', cost={self.total_cost}>"