from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    DELETED = "Deleted"

class CarStatus(str, Enum):
    AVAILABLE = "Available"
    ACTIVE = "Active"         # rented out
    MAINTENANCE = "Maintenance"
    INACTIVE = "Inactive"
    DELETED = "Deleted"

class RentalStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"     # optional, before Active
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"
    DELETED = "Deleted"
