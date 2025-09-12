class Car:
    def __init__(self, id=None, make=None, model=None, year=None, rate=0.0, status="Available"):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.rate = rate
        self.status = status  # Available, Rented, Maintenance, Deleted

    def __repr__(self):
        return f"<Car {self.id}: {self.make} {self.model} ({self.year}) - ${self.rate}/day, Status={self.status}>"
