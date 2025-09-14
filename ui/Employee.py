import getpass
from Contracts.UserDto import UserDto

class UserUI:
    def __init__(self, user_service):
        self._user_service = user_service

    def register_user_ui(self):
        try:
            print("\n=== Register New User ===")
            username = input("Enter username: ")

            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Confirm password: ")

            if password != confirm_password:
                print("Passwords do not match!")
                return

            role = input("Enter role (admin/customer): ")
            name = input("Full name: ")
            contact_number = input("Contact number: ")
            email = input("Email: ")
            address = input("Address: ")

            new_user_dto = UserDto(
                id=None,
                username=username,
                password=password,  # will be hashed in service
                role=role,
                name=name,
                contact_number=contact_number,
                email=email,
                address=address,
                status="Active"
            )

            saved_user = self._user_service.register_user(new_user_dto)
            print(f"User registered successfully: {saved_user.username} ({saved_user.role})")
        except Exception as e:
            print(f"Error registering user: {e}")

    def update_user_ui(self):
        try:
            print("\n=== Update User ===")
            user_id = int(input("Enter User ID to update: "))
            existing = self._user_service.get_by_id(user_id)
            if not existing:
                print("User not found.")
                return

            print("Leave blank to keep current value.")

            username = input(f"Enter new username [{existing.username}]: ") or existing.username
            password = getpass.getpass("Enter new password (leave blank to keep unchanged): ")
            role = input(f"Enter new role [{existing.role}]: ") or existing.role
            name = input(f"Full name [{existing.name}]: ") or existing.name
            contact_number = input(f"Contact number [{existing.contact_number}]: ") or existing.contact_number
            email = input(f"Email [{existing.email}]: ") or existing.email
            address = input(f"Address [{existing.address}]: ") or existing.address
            status = input(f"Enter new status [{existing.status}]: ") or existing.status

            updated_user_dto = UserDto(
                id=user_id,
                username=username,
                password=password if password else existing.password,  # keep old if blank
                role=role,
                name=name,
                contact_number=contact_number,
                email=email,
                address=address,
                status=status
            )

            updated_user = self._user_service.update_user(updated_user_dto)
            if updated_user:
                print(f"User updated: {updated_user.username} ({updated_user.role}), Status={updated_user.status}")
            else:
                print("User not found.")
        except Exception as e:
            print(f"Error updating user: {e}")


    def list_users_ui(self):
        print("\n=== All Users ===")
        users = self._user_service.list_users()
        for u in users:
            print(f"ID {u.id}: {u.username} ({u.role}) - {u.name}, {u.email}, Status={u.status}")

    def delete_user_ui(self):
        try:
            user_id = int(input("Enter User ID to delete: "))
            if self._user_service.delete(user_id):
                print("🗑 User soft deleted.")
            else:
                print("User not found.")
        except Exception as e:
            print(f"Error deleting user: {e}")
