try:
    from car_rental.repository import users_repo
except Exception:
    from repository import users_repo


# -------------------- Authentication --------------------
def login(username: str, password: str):
    return users_repo.login(username, password)


def add_employee(username: str, password: str, role: str = "employee"):
    return users_repo.add_employee(username, password, role)


# -------------------- User Management --------------------
def list_users(include_deleted=False):
    return users_repo.list_users(include_deleted)


def search_users(keyword: str, include_deleted=False):
    return users_repo.search_users(keyword, include_deleted)


def remove_user(user_id, acting_user_id):
    return users_repo.remove_user(user_id, acting_user_id)


def restore_user(user_id, acting_user_id):
    return users_repo.restore_user(user_id, acting_user_id)
