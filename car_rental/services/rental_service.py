
from datetime import date, datetime

try:
    from car_rental.storage import repository as repo
except Exception:
    from storage import repository as repo

class PricingStrategy:
    def compute(self,start:date,end:date,base_rate:float)->float: raise NotImplementedError
    @staticmethod
    def _days_inclusive(start,end): return max(1,(end-start).days+1)
class StandardPricing(PricingStrategy):
    def compute(self,start,end,base_rate): return self._days_inclusive(start,end)*base_rate
class ElectricPricing(PricingStrategy):
    def compute(self,start,end,base_rate): return self._days_inclusive(start,end)*base_rate*0.9
class SUVPricing(PricingStrategy):
    def compute(self,start,end,base_rate): return self._days_inclusive(start,end)*base_rate*1.15

def select_pricing_strategy(vt:str)->PricingStrategy:
    vt=(vt or '').lower()
    if vt=='suv': return SUVPricing()
    if vt in('ev','electric','electric_car'): return ElectricPricing()
    return StandardPricing()

def add_car(make,model,year,vtype,base_rate,user_id): return repo.add_car(make,model,year,vtype,base_rate,user_id)
def update_car(car_id,**kwargs): return repo.update_car(car_id,**kwargs)
def add_customer(name,email,phone): return repo.add_customer(name,email,phone)

def rent_car(car_id,customer_email,start_date,planned_end_date,user_id):
    car=repo.get_car(car_id)
    if not car: raise ValueError("Car not found")
    if car[6]!="available": raise ValueError("Car not available")
    cust=repo.get_customer_by_email(customer_email)
    if not cust: raise ValueError("Customer not found")
    active=repo.get_active_rental_by_car(car_id)
    if active: raise ValueError("Car already rented")
    rid=repo.create_rental(car_id,cust[0],start_date,planned_end_date,user_id)
    repo.set_car_status(car_id,"rented")
    return rid

def return_car(car_id,returned_date,user_id):
    car=repo.get_car(car_id)
    if not car: raise ValueError("Car not found")
    active=repo.get_active_rental_by_car(car_id)
    if not active: raise ValueError("No active rental")
    rental_id,_,_,start_iso,_=active
    start_date=datetime.fromisoformat(start_iso).date()
    strategy=select_pricing_strategy(car[4])
    price=strategy.compute(start_date,returned_date,car[5])
    repo.return_rental(rental_id,returned_date,price,user_id)
    repo.set_car_status(car_id,"available")
    return price

def list_cars(include_unavailable=True): return repo.list_cars(include_unavailable)
def list_customers(): return repo.list_customers()
def list_rentals(active_only=False): return repo.list_rentals(active_only)
