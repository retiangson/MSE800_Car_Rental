class ReceiptPrinter:
    """Utility for printing rental receipts."""

    @staticmethod
    def print_receipt(rental, car, customer, days: int, total_cost: float, title="RECEIPT"):
        """
        Print a formatted rental receipt.

        Args:
            rental: Rental entity object.
            car: Car entity object.
            customer: User entity (customer).
            days (int): Rental duration in days.
            total_cost (float): Total calculated cost.
            title (str): Receipt title (e.g., "INITIAL RECEIPT", "FINAL RECEIPT").
        """
        print(f"\n===== {title} =====")
        print(f"Rental ID   : {rental.id}")
        print(f"Customer    : {customer.name} ({customer.email})")
        print(f"Car         : {car.make} {car.model} ({car.year})")
        print(f"Period      : {rental.start_date} → {rental.end_date} ({days} days)")
        print(f"Rate/Day    : ${car.base_rate:.2f}")
        print(f"Total Cost  : ${total_cost:.2f}")
        print("==========================\n")
