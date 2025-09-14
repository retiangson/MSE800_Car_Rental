from dataclasses import dataclass

@dataclass
class UserDto:
    id: int | None
    username: str
    password: str
    role: str        # admin / customer
    name: str
    contact_number: str | None
    email: str | None
    address: str | None
    status: str      # Active, Deleted, Inactive
