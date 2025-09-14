import getpass
class LoginUI:
    def __init__(self, user_service):
        self._user_service = user_service

    def login_ui(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        user = self._user_service.login_user(username, password)
        if user:
            print(f"Welcome, {user.username}! Role: {user.role}")
            return user   # return the User object
        else:
            print("Invalid login.")
            return None
