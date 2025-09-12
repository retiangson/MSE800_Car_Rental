from Domain.Models.Rental import Rental

def create_rental_ui(rental_service, user):
    try:
        car_id = int(input("Enter Car ID: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        new_rental = Rental(customer_id=user.id, car_id=car_id,
                            start_date=start_date, end_date=end_date,
                            status="Pending")
        rental_service.create_rental(new_rental)

        print("✅ Rental request created (Pending approval).")
    except Exception as e:
        print(f"❌ Error creating rental: {e}")


def list_rentals_ui(rental_service):
    print("\nAll Rentals:")
    rentals = rental_service.list_rentals()
    for r in rentals:
        print(f"Rental {r.id}: Car {r.car_id}, Customer {r.customer_id}, "
              f"{r.start_date} → {r.end_date}, Status: {r.status}")


def list_active_rentals_ui(rental_service):
    print("\nActive Rentals:")
    rentals = rental_service.list_active_rentals()
    for r in rentals:
        print(f"Rental {r.id}: Car {r.car_id}, Customer {r.customer_id}, Status: {r.status}")


def approve_rental_ui(rental_service):
    try:
        rental_id = int(input("Enter Rental ID to approve: "))
        if rental_service.approve_rental(rental_id):
            print("✅ Rental approved.")
        else:
            print("❌ Rental not found.")
    except Exception as e:
        print(f"❌ Error approving rental: {e}")


def reject_rental_ui(rental_service):
    try:
        rental_id = int(input("Enter Rental ID to reject: "))
        if rental_service.reject_rental(rental_id):
            print("🚫 Rental rejected.")
        else:
            print("❌ Rental not found.")
    except Exception as e:
        print(f"❌ Error rejecting rental: {e}")


def cancel_rental_ui(rental_service):
    try:
        rental_id = int(input("Enter Rental ID to cancel: "))
        if rental_service.cancel_rental(rental_id):
            print("🗑 Rental cancelled.")
        else:
            print("❌ Rental not found.")
    except Exception as e:
        print(f"❌ Error cancelling rental: {e}")


def return_rental_ui(rental_service, car_service):
    try:
        rental_id = int(input("Enter Rental ID to return: "))
        if rental_service.complete_rental(rental_id, car_service):
            print("✅ Rental completed. Car is now available.")
        else:
            print("❌ Could not complete rental.")
    except Exception as e:
        print(f"❌ Error returning rental: {e}")
