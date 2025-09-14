from Contracts.RentalDto import RentalDto
from datetime import datetime

class RentalUI:
    def __init__(self, rental_service):
        self._rental_service = rental_service

    def create_rental_ui(self, current_user):
        try:
            print("\n=== Create Rental Request ===")
            car_id = int(input("Enter Car ID: "))
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            dto = RentalDto(
                id=None,
                car_id=car_id,
                user_id=current_user.id,
                start_date=start_date,
                end_date=end_date,
                total_cost=None,
                status=None
            )

            saved = self._rental_service.create_rental(dto)
            print(f"Rental created successfully: ID {saved.id}, Car {saved.car_id}, Status={saved.status}")
        except Exception as e:
            print(f"Error creating rental: {e}")

    def list_rentals_ui(self, include_deleted=False):
        print("\nAll Rentals:")
        rentals = self._rental_service.list_rentals(include_deleted=include_deleted)
        for r in rentals:
            print(f"{r.id}: Car {r.car_id}, Customer {r.user_id}, "
                  f"{r.start_date} → {r.end_date}, Status={r.status}, Total=${r.total_cost}")
            
    def list_customer_rentals_ui(self, current_user, include_deleted=False):
        print(f"\nRental History for {current_user.name}:")
        rentals = self._rental_service.list_rentals_by_customer(
            user_id=current_user.id,
            include_deleted=include_deleted
        )
        if not rentals:
            print("No rentals found.")
            return
        for r in rentals:
            print(f"{r.id}: Car {r.car_id}, {r.start_date} → {r.end_date}, "
                f"Status={r.status}, Total=${r.total_cost}")
        
    def list_active_rentals_ui(self):
        print("\nActive Rentals:")
        rentals = self._rental_service.list_active_rentals()
        for r in rentals:
            print(f"{r.id}: Car {r.car_id}, Customer {r.user_id}, "
                  f"{r.start_date} → {r.end_date}, Status={r.status}, Total=${r.total_cost}")

    def approve_rental_ui(self):
        try:
            rental_id = int(input("Enter Rental ID to approve and start: "))
            if self._rental_service.approve_and_start_rental(rental_id):
                print("Rental approved and started.")
            else:
                print("Rental not found or invalid.")
        except Exception as e:
            print(f"Error approving rental: {e}")

    def reject_rental_ui(self):
        try:
            rental_id = int(input("Enter Rental ID to reject: "))
            if self._rental_service.reject_rental(rental_id):
                print("Rental rejected.")
            else:
                print("Rental not found.")
        except Exception as e:
            print(f"Error rejecting rental: {e}")

    def complete_rental_ui(self):
        try:
            rental_id = int(input("Enter Rental ID to complete: "))
            return_date = input("Enter actual return date (YYYY-MM-DD): ")
            actual_return = datetime.strptime(return_date, "%Y-%m-%d")
            if self._rental_service.complete_rental(rental_id, actual_return):
                print("Rental completed.")
            else:
                print("Rental not found or invalid.")
        except Exception as e:
            print(f"Error completing rental: {e}")

    def cancel_rental_ui(self):
        try:
            rental_id = int(input("Enter Rental ID to cancel: "))
            if self._rental_service.cancel_rental(rental_id):
                print("Rental cancelled.")
            else:
                print("Rental not found.")
        except Exception as e:
            print(f"Error cancelling rental: {e}")

    def delete_rental_ui(self):
        try:
            rental_id = int(input("Enter Rental ID to soft delete: "))
            if self._rental_service.delete_rental(rental_id):
                print("Rental marked as Deleted.")
            else:
                print("Rental not found.")
        except Exception as e:
            print(f"Error deleting rental: {e}")
