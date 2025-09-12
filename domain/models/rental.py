class Rental:
    def __init__(self, id=None, customer_id=None, car_id=None, start_date=None, end_date=None,
                 status="Pending", total_cost=0):
        self.id = id
        self.customer_id = customer_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        # Workflow status
        # Options: Pending, Approved, Rejected, Active, Completed, Cancelled, Deleted
        self.status = status
        self.total_cost = total_cost  # store calculated cost

    def __repr__(self):
        return (f"<Rental {self.id}: Car {self.car_id}, Customer {self.customer_id}, "
                f"{self.start_date} → {self.end_date}, Status={self.status}, "
                f"Total=${self.total_cost:.2f}>")
