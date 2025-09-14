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
