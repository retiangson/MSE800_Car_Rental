import getpass
from Contracts.UserDto import UserDto

class CustomerUI:
    def __init__(self, user_service):
        self._user_service = user_service

    def customer_register_ui(self):
        try:
            print("\n=== Customer Registration ===")
            username = input("Choose username: ")

            password = getpass.getpass("Choose password: ")
            confirm_password = getpass.getpass("Confirm password: ")

            if password != confirm_password:
                print("Passwords do not match!")
                return

            name = input("Full name: ")
            contact_number = input("Contact number: ")
            email = input("Email: ")
            address = input("Address: ")

            new_user_dto = UserDto(
                id=None,
                username=username,
                password=password,  # raw, will be hashed in service
                role="customer",
                name=name,
                contact_number=contact_number,
                email=email,
                address=address,
                status="Active"
            )

            saved_user = self._user_service.register_user(new_user_dto)
            print(f"Customer registered successfully: {saved_user.username} ({saved_user.role})")
        except Exception as e:
            print(f"Error registering customer: {e}")
