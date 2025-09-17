import getpass
from Contracts.UserDto import UserDto
from Contracts.Enums.StatusEnums import UserStatus  

class CustomerUI:
    """UI layer for customer-related actions (registration)."""

    def __init__(self, user_service):
        """Initialize with UserService dependency."""
        self._user_service = user_service

    def customer_register_ui(self, max_attempts: int = 3):
        """Prompt customer for details and register a new account with validation."""
        print("\n=== Customer Registration ===")

        attempts = 0
        while attempts < max_attempts:
            try:
                username = input("Choose username: ").strip()
                if not username:
                    print("❌ Username cannot be empty.")
                    attempts += 1
                    continue

                # Secure password input
                password = getpass.getpass("Choose password: ").strip()
                confirm_password = getpass.getpass("Confirm password: ").strip()

                if not password:
                    print("❌ Password cannot be empty.")
                    attempts += 1
                    continue

                if password != confirm_password:
                    print("❌ Passwords do not match. Try again.")
                    attempts += 1
                    continue

                name = input("Full name: ").strip()
                if not name:
                    print("❌ Full name cannot be empty.")
                    attempts += 1
                    continue

                contact_number = input("Contact number: ").strip()
                email = input("Email: ").strip()
                address = input("Address: ").strip()

                new_user_dto = UserDto(
                    id=None,
                    username=username,
                    password=password,  # Raw, will be hashed in service
                    role="customer",
                    name=name,
                    contact_number=contact_number,
                    email=email,
                    address=address,
                    status=UserStatus.ACTIVE
                )

                saved_user = self._user_service.register_user(new_user_dto)
                print(f"✅ Customer registered successfully: {saved_user.username} ({saved_user.role.value})")
                return saved_user

            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ Registration cancelled. Returning to main menu.")
                return None
            except Exception as e:
                print(f"❌ Error registering customer: {e}")
                return None

        print("⚠️ Too many failed attempts. Returning to main menu.")
        return None
