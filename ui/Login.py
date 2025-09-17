import getpass

class LoginUI:
    """UI layer for user login."""

    def __init__(self, user_service):
        """Initialize with UserService dependency."""
        self._user_service = user_service

    def login_ui(self, max_attempts: int = 3):
        """Prompt for username and password, authenticate user with retries."""
        attempts = 0
        while attempts < max_attempts:
            try:
                username = input("Username: ").strip()
                if not username:
                    print("Username cannot be empty.")
                    continue

                password = getpass.getpass("Password: ").strip()
                if not password:
                    print("Password cannot be empty.")
                    continue

                user = self._user_service.login_user(username, password)
                if user:
                    print(f"Welcome, {user.username}! Role: {user.role}")
                    return user   # Return the authenticated UserDto
                else:
                    print("Invalid username or password. Please try again.")

            except (EOFError, KeyboardInterrupt):
                print("\nLogin cancelled. Returning to main menu.")
                return None
            except Exception as e:
                print(f"Unexpected error during login: {e}")
                return None

            attempts += 1

        print("Too many failed login attempts. Returning to main menu.")
        return None
