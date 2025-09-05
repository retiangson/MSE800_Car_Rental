
# Car Rental System (CLI) — MSE800 Assessment 1

A **Command-line Car Rental Management System** built in Python for **MSE800 Software Engineering**.  
Demonstrates **OOP principles** (encapsulation, abstraction, inheritance, polymorphism), the **Strategy Design Pattern** for pricing, and **Role-Based Access Control (RBAC)** with audit logging.

---

## Features
- **Role-based login system**:
  - **Manager**: full access (manage cars, employees, customers, rentals).  
  - **Employee**: limited access (manage customers, rent/return cars, search).  

- **Car Management**
  - Add cars, edit cars, list cars, search cars.  
  - Track **who created/updated** cars and when.  

- **Customer Management**
  - Add, list, and search customers.  

- **Employee Management**
  - Add employees (with roles).  
  - List/search employees.  

- **Rental Management**
  - Rent and return cars.  
  - Pricing via **Strategy Pattern**:  
    - Standard  
    - Electric (10% discount)  
    - SUV (15% surcharge)  
  - Track **who created/updated** rentals and when.  

- **Search**
  - Search cars (by make/model/year/type).  
  - Search customers (by name/email).  
  - Search employees (by username/role).  
  - Search rentals (by car, customer, status).  

- **Audit Logging**
  - `date_created`, `date_updated`, `created_by`, and `updated_by` for **cars** and **rentals**.  
  - Provides accountability for all operations.

---

## Database Schema

### **users**
- `id` (PK)  
- `username` (unique)  
- `password`  
- `role` (manager/employee)  

### **cars**
- `id` (PK)  
- `make`, `model`, `year`, `type`, `base_rate`, `status`  
- `date_created`, `date_updated`  
- `created_by` (FK → users.id)  
- `updated_by` (FK → users.id)  

### **customers**
- `id` (PK)  
- `name`, `email` (unique), `phone`  

### **rentals**
- `id` (PK)  
- `car_id` (FK → cars.id)  
- `customer_id` (FK → customers.id)  
- `start_date`, `planned_end_date`, `returned_date`, `total_price`  
- `date_created`, `date_updated`  
- `created_by` (FK → users.id)  
- `updated_by` (FK → users.id)  
![Database ERD](Database_Relationship_Diagram.png)
---

## Default Logins
- **Manager**: `admin / admin`  
- **Employee**: `employee / employee`  

---

## How to Run
From the folder containing `car_rental/`, run either:

```bash
# Option A: package mode (recommended)
python -m car_rental.main

# Option B: script mode
cd car_rental
python main.py
```

SQLite database (`car_rental.db`) initializes automatically with default users.

---

## Example Menus

### Manager
```
1) Add car
2) List cars
3) Search car
4) Edit car
5) Add customer
6) List customers
7) Search customer
8) Add employee
9) List employees
10) Search employee
11) Rent a car
12) Return a car
13) List rentals
14) Search rentals
0) Exit
```

### Employee
```
1) List cars
2) Search car
3) Add customer
4) List customers
5) Search customer
6) Rent a car
7) Return a car
8) List rentals
9) Search rentals
0) Exit
```

---

## Design Pattern
**Strategy Pattern** is used for rental pricing:  
- `StandardPricing` → regular price  
- `ElectricPricing` → 10% discount  
- `SUVPricing` → 15% surcharge  

---

## Notes
- No external dependencies; only Python standard library.  
- Cross-platform (Windows, macOS, Linux).  
- Requirements are listed in `requirements.txt` (empty, since no pip installs are needed).  
