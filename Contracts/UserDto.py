from dataclasses import dataclass

@dataclass
class UserDto:
    """Data Transfer Object for User entity."""

    id: int | None              # Unique identifier (None for new users not yet saved)
    username: str               # Unique login name
    password: str               # Plaintext (from UI) or hashed password
    role: str                   # User role (admin / customer)
    name: str                   # Full display name
    contact_number: str | None  # Optional contact number
    email: str | None           # Optional email address
    address: str | None         # Optional address
    status: str                 # Lifecycle status (Active, Deleted, Inactive)
