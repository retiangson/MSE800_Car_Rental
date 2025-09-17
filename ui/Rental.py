from Contracts.RentalDto import RentalDto
from Contracts.Enums.StatusEnums import RentalStatus  # ✅ enum
from datetime import datetime

def safe_int_input(prompt: str) -> int:
    """Ensure user enters a valid integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ Please enter a valid number.")

def safe_date_input(prompt: str) -> str:
    """Ensure user enters a valid date in YYYY-MM-DD format."""
    while True:
        try:
            date_str = input(prompt).strip()
            datetime.strptime(date_str, "%Y-%m-%d")  # validate
            return date_str
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD.")

class RentalUI:
    """UI layer for managing rentals (create, approve, reject, complete, cancel, delete)."""

    def __init__(self, rental_service):
        self._rental_service = rental_service

    def create_rental_ui(self, current_user):
        """Prompt customer to create a rental request."""
        try:
            print("\n=== Create Rental Request ===")
            car_id = safe_int_input("Enter Car ID: ")
            start_date = safe_date_input("Enter start date (YYYY-MM-DD): ")
            end_date = safe_date_input("Enter end date (YYYY-MM-DD): ")

            dto = RentalDto(
                id=None,
                car_id=car_id,
                user_id=current_user.id,
                start_date=start_date,
                end_date=end_date,
                total_cost=None,
                status=RentalStatus.PENDING  # ✅ default
            )

            saved = self._rental_service.create_rental(dto)
            print(f"✅ Rental created: ID {saved.id}, Car {saved.car_id}, Status={saved.status.value}")
        except Exception as e:
            print(f"❌ Error creating rental: {e}")

    def list_rentals_ui(self, include_deleted=False):
        """List all rentals (optionally include deleted)."""
        print("\n📋 All Rentals:")
        try:
            rentals = self._rental_service.list_rentals(include_deleted=include_deleted)
            if not rentals:
                print("⚠️ No rentals found.")
                return
            for r in rentals:
                print(f"{r.id}: Car {r.car_id}, Customer {r.user_id}, "
                      f"{r.start_date} → {r.end_date}, Status={r.status.value}, Total=${r.total_cost}")
        except Exception as e:
            print(f"❌ Error listing rentals: {e}")

    def list_customer_rentals_ui(self, current_user, include_deleted=False):
        """List all rentals for the current customer."""
        print(f"\n📋 Rental History for {current_user.name}:")
        try:
            rentals = self._rental_service.list_rentals_by_customer(
                user_id=current_user.id,
                include_deleted=include_deleted
            )
            if not rentals:
                print("⚠️ No rentals found.")
                return
            for r in rentals:
                print(f"{r.id}: Car {r.car_id}, {r.start_date} → {r.end_date}, "
                      f"Status={r.status.value}, Total=${r.total_cost}")
        except Exception as e:
            print(f"❌ Error listing customer rentals: {e}")

    def list_active_rentals_ui(self):
        """List all currently active rentals."""
        print("\n🚗 Active Rentals:")
        try:
            rentals = self._rental_service.list_active_rentals()
            if not rentals:
                print("⚠️ No active rentals.")
                return
            for r in rentals:
                print(f"{r.id}: Car {r.car_id}, Customer {r.user_id}, "
                      f"{r.start_date} → {r.end_date}, Status={r.status.value}, Total=${r.total_cost}")
        except Exception as e:
            print(f"❌ Error listing active rentals: {e}")

    def list_customer_active_rentals_ui(self, current_user):
        """List only active rentals for the current customer."""
        print(f"\n🚗 Active Rentals for {current_user.name}:")
        try:
            rentals = self._rental_service.list_rentals_by_customer(user_id=current_user.id)
            active = [r for r in rentals if r.status == RentalStatus.ACTIVE]
            if not active:
                print("⚠️ No active rentals found for your account.")
                return
            for r in active:
                print(f"{r.id}: Car {r.car_id}, {r.start_date} → {r.end_date}, "
                      f"Status={r.status.value}, Total=${r.total_cost}")
        except Exception as e:
            print(f"❌ Error listing customer active rentals: {e}")

    def approve_rental_ui(self):
        """Approve and start a rental request (shows all pending first)."""
        try:
            print("\n📋 Pending Rentals:")
            pending = self._rental_service.get_rentals_by_status(RentalStatus.PENDING)

            if not pending:
                print("⚠️ No pending rentals available for approval.")
                return

            for r in pending:
                print(f"ID {r.id}: Car {r.car_id}, Customer {r.user_id}, "
                      f"{r.start_date} → {r.end_date}, Status={r.status.value}")

            rental_id = int(input("\nEnter Rental ID to approve and start: "))
            if self._rental_service.approve_and_start_rental(rental_id):
                print("✅ Rental approved and started.")
            else:
                print("⚠️ Rental not found or invalid.")
        except Exception as e:
            print(f"❌ Error approving rental: {e}")

    def reject_rental_ui(self):
        """Reject a rental request (shows all pending first)."""
        try:
            print("\n📋 Pending Rentals:")
            pending = self._rental_service.get_rentals_by_status(RentalStatus.PENDING)

            if not pending:
                print("⚠️ No pending rentals available to reject.")
                return

            for r in pending:
                print(f"ID {r.id}: Car {r.car_id}, Customer {r.user_id}, "
                      f"{r.start_date} → {r.end_date}, Status={r.status.value}")

            rental_id = int(input("\nEnter Rental ID to reject: "))
            if self._rental_service.reject_rental(rental_id):
                print("🚫 Rental rejected.")
            else:
                print("⚠️ Rental not found.")
        except Exception as e:
            print(f"❌ Error rejecting rental: {e}")

    def complete_rental_ui(self):
        """Complete a rental and calculate final cost."""
        try:
            rental_id = safe_int_input("Enter Rental ID to complete: ")
            return_date = safe_date_input("Enter actual return date (YYYY-MM-DD): ")
            actual_return = datetime.strptime(return_date, "%Y-%m-%d")

            if self._rental_service.complete_rental(rental_id, actual_return):
                print("✅ Rental completed successfully.")
            else:
                print("⚠️ Rental not found or invalid.")
        except Exception as e:
            print(f"❌ Error completing rental: {e}")

    def cancel_rental_ui(self):
        """Cancel a rental request."""
        try:
            rental_id = safe_int_input("Enter Rental ID to cancel: ")
            if self._rental_service.cancel_rental(rental_id):
                print("🛑 Rental cancelled.")
            else:
                print("⚠️ Rental not found.")
        except Exception as e:
            print(f"❌ Error cancelling rental: {e}")

    def delete_rental_ui(self):
        """Soft delete a rental (mark as Deleted)."""
        try:
            rental_id = safe_int_input("Enter Rental ID to soft delete: ")
            if self._rental_service.delete_rental(rental_id):
                print("🗑 Rental marked as Deleted.")
            else:
                print("⚠️ Rental not found.")
        except Exception as e:
            print(f"❌ Error deleting rental: {e}")
