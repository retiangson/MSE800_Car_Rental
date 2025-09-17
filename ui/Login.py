import getpass

class LoginUI:
    """UI layer for user login."""

    def __init__(self, user_service):
        """Initialize with UserService dependency."""
        self._user_service = user_service

    def login_ui(self):
        """Prompt for username and password, authenticate user."""
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        user = self._user_service.login_user(username, password)
        if user:
            print(f"Welcome, {user.username}! Role: {user.role}")
            return user   # Return the authenticated UserDto
        else:
            print("Invalid login.")
            return None
