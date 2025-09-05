try:
    from car_rental.repository import customers_repo as repo
except Exception:
    from repository import customers_repo as repo



def add_customer(name, email, phone):
    return repo.add_customer(name, email, phone)


def list_customers(include_deleted=False):
    return repo.list_customers(include_deleted)


def search_customers(keyword: str, include_deleted=False):
    return repo.search_customers(keyword, include_deleted)


def remove_customer(customer_id, user_id):
    return repo.remove_customer(customer_id, user_id)


def restore_customer(customer_id, user_id):
    return repo.restore_customer(customer_id, user_id)
