from datetime import date, datetime

try:
    from car_rental.repository import cars_repo, customers_repo, rentals_repo
except Exception:
    from repository import cars_repo, customers_repo, rentals_repo


# -------------------- Pricing Strategies --------------------
class PricingStrategy:
    def compute(self, start: date, end: date, base_rate: float) -> float:
        raise NotImplementedError

    @staticmethod
    def _days_inclusive(start, end):
        return max(1, (end - start).days + 1)


class StandardPricing(PricingStrategy):
    def compute(self, start, end, base_rate):
        return self._days_inclusive(start, end) * base_rate


class ElectricPricing(PricingStrategy):
    def compute(self, start, end, base_rate):
        return self._days_inclusive(start, end) * base_rate * 0.9


class SUVPricing(PricingStrategy):
    def compute(self, start, end, base_rate):
        return self._days_inclusive(start, end) * base_rate * 1.15


def select_pricing_strategy(vt: str) -> PricingStrategy:
    vt = (vt or '').lower()
    if vt == 'suv':
        return SUVPricing()
    if vt in ('ev', 'electric', 'electric_car'):
        return ElectricPricing()
    return StandardPricing()


# -------------------- Rentals --------------------
def rent_car(car_id, customer_email, start_date, planned_end_date, user_id):
    car = cars_repo.get_car(car_id)
    if not car:
        raise ValueError("Car not found")
    if car[6] != "available":
        raise ValueError("Car not available")

    cust = customers_repo.get_customer_by_email(customer_email)
    if not cust:
        raise ValueError("Customer not found")

    active = rentals_repo.get_active_rental_by_car(car_id)
    if active:
        raise ValueError("Car already rented")

    rid = rentals_repo.create_rental(car_id, cust[0], start_date, planned_end_date, user_id)
    cars_repo.set_car_status(car_id, "rented")
    return rid


def return_car(car_id, returned_date, user_id):
    car = cars_repo.get_car(car_id)
    if not car:
        raise ValueError("Car not found")

    active = rentals_repo.get_active_rental_by_car(car_id)
    if not active:
        raise ValueError("No active rental")

    rental_id, _, _, start_iso, _ = active
    start_date = datetime.fromisoformat(start_iso).date()

    strategy = select_pricing_strategy(car[4])
    price = strategy.compute(start_date, returned_date, car[5])

    rentals_repo.return_rental(rental_id, returned_date, price, user_id)
    cars_repo.set_car_status(car_id, "available")
    return price


def list_rentals(active_only=False, include_deleted=False):
    return rentals_repo.list_rentals(active_only, include_deleted)


def search_rentals(car_id=None, customer_id=None, active_only=None, include_deleted=False):
    return rentals_repo.search_rentals(car_id, customer_id, active_only, include_deleted)
