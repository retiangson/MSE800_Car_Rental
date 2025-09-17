import getpass
from Contracts.UserDto import UserDto
from Contracts.Enums.StatusEnums import UserStatus

def safe_int_input(prompt: str) -> int:
    """Ensure user enters a valid integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ Please enter a valid number.")

class UserUI:
    """UI layer for admin/employee user management (create, update, list, delete)."""

    def __init__(self, user_service):
        self._user_service = user_service

    def register_user_ui(self):
        """Prompt admin to register a new user (admin or customer)."""
        try:
            print("\n=== Register New User ===")
            username = input("Enter username: ").strip()
            if not username:
                print("❌ Username cannot be empty.")
                return

            password = getpass.getpass("Enter password: ").strip()
            confirm_password = getpass.getpass("Confirm password: ").strip()

            if not password:
                print("❌ Password cannot be empty.")
                return
            if password != confirm_password:
                print("❌ Passwords do not match.")
                return

            # Role selection via enum
            role_input = input("Enter role (admin/customer): ").strip().lower()
            if role_input == "admin":
                role = "admin"
            elif role_input == "customer":
                role = "customer"
            else:
                print("❌ Role must be 'admin' or 'customer'.")
                return

            name = input("Full name: ").strip()
            contact_number = input("Contact number: ").strip()
            email = input("Email: ").strip()
            address = input("Address: ").strip()

            new_user_dto = UserDto(
                id=None,
                username=username,
                password=password,  # Will be hashed in service
                role=role,
                name=name,
                contact_number=contact_number,
                email=email,
                address=address,
                status=UserStatus.ACTIVE  # ✅ default enum
            )

            saved_user = self._user_service.register_user(new_user_dto)
            print(f"✅ User registered: {saved_user.username} ({saved_user.role.value})")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ Registration cancelled.")
        except Exception as e:
            print(f"❌ Error registering user: {e}")

    def update_user_ui(self):
        """Prompt admin to update an existing user's details."""
        try:
            print("\n=== Update User ===")
            user_id = safe_int_input("Enter User ID to update: ")
            existing = self._user_service.get_by_id(user_id)
            if not existing:
                print("⚠️ User not found.")
                return

            print("Leave blank to keep current value.")

            username = input(f"Enter new username [{existing.username}]: ").strip() or existing.username
            password = getpass.getpass("Enter new password (leave blank to keep unchanged): ").strip()

            # Role update (optional, keep enum safe)
            role_input = input(f"Enter new role [{existing.role.value}]: ").strip().lower()
            if not role_input:
                role = existing.role
            elif role_input == "admin":
                role = "admin"
            elif role_input == "customer":
                role = "customer"
            else:
                print("❌ Invalid role, keeping current.")
                role = existing.role

            name = input(f"Full name [{existing.name}]: ").strip() or existing.name
            contact_number = input(f"Contact number [{existing.contact_number}]: ").strip() or existing.contact_number
            email = input(f"Email [{existing.email}]: ").strip() or existing.email
            address = input(f"Address [{existing.address}]: ").strip() or existing.address

            # Status update (optional, keep enum safe)
            status_input = input(f"Enter new status [{existing.status.value}]: ").strip().capitalize()
            if not status_input:
                status = existing.status
            else:
                try:
                    status = UserStatus(status_input)
                except ValueError:
                    print("❌ Invalid status, keeping current.")
                    status = existing.status

            updated_user_dto = UserDto(
                id=user_id,
                username=username,
                password=password if password else existing.password,
                role=role,
                name=name,
                contact_number=contact_number,
                email=email,
                address=address,
                status=status
            )

            updated_user = self._user_service.update_user(updated_user_dto)
            if updated_user:
                print(f"✅ User updated: {updated_user.username} ({updated_user.role.value}), Status={updated_user.status.value}")
            else:
                print("⚠️ User not found.")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ Update cancelled.")
        except Exception as e:
            print(f"❌ Error updating user: {e}")

    def list_users_ui(self):
        """Display all users in the system."""
        print("\n=== All Users ===")
        try:
            users = self._user_service.list_users()
            if not users:
                print("⚠️ No users found.")
                return
            for u in users:
                print(f"ID {u.id}: {u.username} ({u.role}) - {u.name}, {u.email}, Status={u.status.value}")
        except Exception as e:
            print(f"❌ Error listing users: {e}")

    def delete_user_ui(self):
        """Soft delete a user (mark as Deleted)."""
        try:
            user_id = safe_int_input("Enter User ID to delete: ")
            if self._user_service.delete(user_id):
                print("🗑 User soft deleted.")
            else:
                print("⚠️ User not found.")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ Delete cancelled.")
        except Exception as e:
            print(f"❌ Error deleting user: {e}")
