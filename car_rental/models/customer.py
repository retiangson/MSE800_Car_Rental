
class Customer:
    """Simple data model showing encapsulation."""
    def __init__(self, name: str, email: str, phone: str):
        self._name = name
        self._email = email
        self._phone = phone

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> str:
        return self._phone

    def __str__(self) -> str:
        return f"{self.name} <{self.email}> ({self.phone})"
