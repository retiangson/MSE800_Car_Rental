from Domain.Models.Rental import Rental
from datetime import datetime

def create_rental_ui(rental_service, user):
    try:
        car_id = int(input("Enter Car ID: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        new_rental = Rental(
            customer_id=user.id,
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            status="Pending",
            total_cost=0
        )
        rental_service.create_rental(new_rental)

        print("Rental request created (Pending approval).")
    except Exception as e:
        print(f"Error creating rental: {e}")


def list_rentals_ui(rental_service):
    print("\nAll Rentals:")
    rentals = rental_service.list_rentals()
    for r in rentals:
        print(f"Rental {r.id}: Car {r.car_id}, Customer {r.customer_id}, "
              f"{r.start_date} → {r.end_date}, Status: {r.status}, "
              f"Total=${r.total_cost:.2f}")


def list_active_rentals_ui(rental_service):
    print("\nActive Rentals:")
    rentals = rental_service.list_active_rentals()
    for r in rentals:
        print(f"Rental {r.id}: Car {r.car_id}, Customer {r.customer_id}, "
              f"Status: {r.status}, Total=${r.total_cost:.2f}")


def approve_and_start_rental_ui(rental_service):
    """Approve and immediately start rental, then print receipt."""
    try:
        rental_id = int(input("Enter Rental ID to approve & start: "))
        if rental_service.approve_and_start_rental(rental_id):
            print("Rental approved and started. Receipt generated below:")
        else:
            print("Rental not found or could not be started.")
    except Exception as e:
        print(f"Error approving & starting rental: {e}")


def reject_rental_ui(rental_service):
    try:
        rental_id = int(input("Enter Rental ID to reject: "))
        if rental_service.reject_rental(rental_id):
            print("Rental rejected.")
        else:
            print("Rental not found.")
    except Exception as e:
        print(f"Error rejecting rental: {e}")


def cancel_rental_ui(rental_service):
    try:
        rental_id = int(input("Enter Rental ID to cancel: "))
        if rental_service.cancel_rental(rental_id):
            print("Rental cancelled.")
        else:
            print("Rental not found.")
    except Exception as e:
        print(f"Error cancelling rental: {e}")


def return_rental_ui(rental_service):
    """Complete rental, recalc actual cost based on entered return date, and print final receipt."""
    try:
        rental_id = int(input("Enter Rental ID to return: "))
        rental = rental_service.repo.find_by_id(rental_id)

        if not rental:
            print("Rental not found.")
            return

        if rental.status != "Active":
            print(f"Cannot return rental with status '{rental.status}'. Only Active rentals can be returned.")
            return

        # Ask for actual return date
        actual_return_date = input("Enter actual return date (YYYY-MM-DD): ")
        try:
            actual_return = datetime.strptime(actual_return_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if rental_service.complete_rental(rental_id, actual_return):
            print("Rental completed. Car is now available. Final receipt generated below:")
        else:
            print("Could not complete rental.")
    except Exception as e:
        print(f"Error returning rental: {e}")
