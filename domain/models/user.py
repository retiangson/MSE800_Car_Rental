# Domain/Models/User.py
from sqlalchemy import Column, Integer, String
from Domain.Repositories.DBManager import Base

class User(Base):
    """
    ORM model representing a system user in the Car Rental System.

    This table stores both customers and admins. 
    Roles determine access control (e.g., only admins can manage cars and rentals).

    Attributes:
        id (int): Primary key, auto-incrementing unique identifier.
        username (str): Unique username for login.
        password (str): Hashed password (stored securely, never in plain text).
        role (str): Role of the user (default = "customer", options: "customer", "admin").
        name (str): Full name of the user.
        contact_number (str): Optional contact number.
        email (str): Optional email address.
        address (str): Optional physical address.
        status (str): User status ("Active", "Deleted", "Inactive").
    """

    __tablename__ = "users" # Database table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False) # Must be unique for login
    password = Column(String, nullable=False)   # hashed password
    role = Column(String, nullable=False, default="customer")  # customer or admin
    name = Column(String, nullable=False) # Display name
    contact_number = Column(String, nullable=True) # Optional field
    email = Column(String, nullable=True) # Optional field
    address = Column(String, nullable=True) # Optional field
    status = Column(String, default="Active")   # Active, Deleted, Inactive

    def __repr__(self):
        """
        String representation for debugging/logging.
        Example:
            <User id=1, username='admin', role='admin', status='Active'>
        """
        return f"<User id={self.id}, username='{self.username}', role='{self.role}', status='{self.status}'>"