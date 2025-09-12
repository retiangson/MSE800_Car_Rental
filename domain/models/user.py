class User:
    def __init__(self, id=None, username=None, password=None, role="customer",
                 name=None, contact_number=None, email=None, address=None,
                 isActive=1, isDeleted=0):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.address = address
        self.isActive = bool(isActive)
        self.isDeleted = bool(isDeleted)

    def __repr__(self):
        return f"<User {self.id}: {self.username} ({self.role})>"
