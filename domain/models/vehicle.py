class Vehicle:
    def __init__(self, id=None, make=None, model=None, year=None, isActive=1, isDeleted=0):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.isActive = bool(isActive)
        self.isDeleted = bool(isDeleted)

    def __repr__(self):
        return f"<Vehicle {self.id}: {self.make} {self.model} ({self.year})>"
