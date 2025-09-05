try:
    from car_rental.storage import cars_repo as repo
except Exception:
    from storage import cars_repo as repo


def add_car(make, model, year, vtype, base_rate, user_id):
    return repo.add_car(make, model, year, vtype, base_rate, user_id)


def update_car(car_id, **kwargs):
    return repo.update_car(car_id, **kwargs)


def list_cars(include_unavailable=True, include_deleted=False):
    return repo.list_cars(include_unavailable, include_deleted)


def list_deleted_cars():
    return repo.list_deleted_cars()

def search_cars(keyword: str, include_deleted=False):
    return repo.search_cars(keyword, include_deleted)

def remove_car(car_id: int, user_id: int):
    return repo.remove_car(car_id, user_id)   # soft delete

def restore_car(car_id: int, user_id: int):
    return repo.restore_car(car_id, user_id)