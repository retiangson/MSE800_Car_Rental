
from datetime import date

class Rental:
    """Rental entity; business object separate from storage concerns."""
    def __init__(self, car_id: int, customer_id: int, start_date: date, planned_end_date=None):
        self.car_id = car_id
        self.customer_id = customer_id
        self.start_date = start_date
        self.planned_end_date = planned_end_date
        self.returned_date = None
        self.total_price = None
