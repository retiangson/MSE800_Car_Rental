# 🚗 Car Rental System – User Documentation  

## 📌 Overview  
The **Car Rental System** is a Python-based application designed to automate the rental process for a car rental company.  
It replaces manual paperwork with a digital solution that supports **user management, car management, rental booking, and rental lifecycle management**.  

The system follows **Object-Oriented Programming (OOP)** principles, **layered architecture**, and **design patterns** (Repository, Service Layer, DTOs, Singleton for DB Manager).  

---

Great idea 👍 I’ll integrate this into your **“Running the Application”** section so users have all 4 options:

1. CLI
2. Executable build
3. API Server
4. Prebuilt ZIP (standalone)

And I’ll also add an **“Initial Admin Access”** section so users know the default login credentials.

Here’s the improved version for your README:

---

## ⚙️ Installation & Configuration

### 1. Requirements

* Python 3.10+
* Virtual environment (recommended)
* Dependencies in `requirements.txt`

### 2. Setup Steps

```bash
# Clone the repository or extract the ZIP
git clone https://github.com/<your-repo>/CarRentalSystem.git
cd CarRentalSystem

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. 🚀 Running the Application

You have multiple ways to run the system:

### **Option A: CLI Mode**

```bash
python main.py
```

This launches the **Main Menu** in console mode.

---

### **Option B: Build as Executable**

```bash
pyinstaller --onefile --console main.py
```

This creates a standalone executable in the `dist/` folder.

Run it with:

```bash
dist/main.exe   # On Windows
```

---

### **Option C: Run API Server (Admin Only)**

From the Admin Main Menu → choose **Run API Server**, or run manually:

```bash
uvicorn api.main:app --reload
```

Server starts at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

API Docs:

* Swagger → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### **Option D: Prebuilt Standalone Package**

Download `car_rental_standalone.zip`, extract it, and run:

```bash
car_rental.exe
```

This version does not require Python or dependencies.

---

## 🔑 Initial Admin Access

When you first run the system, it will automatically seed a default **Admin user** if no users exist.

* **Username:** `admin`
* **Password:** `admin`

⚠️ It is recommended to log in as Admin immediately and **create new users** for proper role management.

---

## 📂 Project Structure & File Purpose  

```
MSE800_Car_Rental/
│── main.py                # Entry point – loads Main Menu
│
├── ui/                    # User Interface Layer
│   ├── MainMenu.py        # Admin & Customer main navigation
│   ├── Car.py             # Add/List/Delete/Restore cars
│   ├── Rental.py          # Create/Approve/Return/Cancel rentals
│   ├── Login.py           # Login screen
│   ├── Customer.py        # Customer registration UI
│   └── Employee.py        # Admin (user management)
│
├── Business/              # Service Layer
│   ├── Services/
│   │   ├── CarService.py
│   │   ├── RentalService.py
│   │   └── UserService.py
│   └── Interfaces/        # Service Interfaces (Abstraction)
│
├── Domain/                # Domain Layer
│   ├── Models/            # Core entities: User, Car, Rental, Vehicle
│   ├── DTOs/              # Data Transfer Objects
│   ├── Mappers/           # Map Models ↔ DTOs
│   ├── Repositories/      # Database access (UserRepo, CarRepo, RentalRepo)
│   └── DBManager.py       # Singleton DB session manager
│
├── tests/                 # Unit tests (pytest)
│
├── requirements.txt       # Dependencies
├── README.md              # User Documentation
└── LICENSE                # License terms
```

**File Purposes:**  
- **UI** → Handles input/output and menus.  
- **Business/Services** → Business logic (rules like "only available cars can be rented").  
- **Domain** → Entities, DTOs, Mappers, Repositories, DB connection.  
- **Tests** → Ensure reliability.  
- **main.py** → Entry point.  

---

## 👥 Roles & Features  

### Admin Features  
- Manage Users (register, list, soft-delete)  
- Manage Cars (add, update, delete, restore, list available cars)  
- Manage Rentals (approve, reject, start, cancel, return)  
- Run API Server  

### Customer Features  
- Register / Login  
- Browse available cars  
- Create rental & preview fees  
- View rental history  

---

## 📊 System Design  

- **Use Case Diagram:** shows Admin & Customer interactions  
- **Sequence Diagram:** illustrates request → UI → Service → Database flow  
- **Class Diagram:** represents layered architecture (UI, Services, Repositories, DTOs, Models)  

---

## 📜 License  

This project is released under the **MIT License**:  
- ✅ Free to use, modify, and distribute.  
- ❌ No warranty provided.  

See full text in `LICENSE` file.  

---

## 🐞 Known Issues / Bugs  

- UI currently runs in console only (no GUI frontend).  
- Database defaults to SQLite (`car_rental.db`). Multi-user concurrency may need PostgreSQL or MySQL.  
- Limited validation on rental dates (future enhancement).  
- No payment integration yet (future feature).  

---

## 👨‍💻 Developer Credit  

**Car Rental System** was developed by:  

**Name:** Ronald Ephraim Tiangson  
**Programme:** Master of Software Engineering (MSE800)  
**Institution:** Yoobee College, New Zealand  
**Date:** September 2025  
**Contact:** [your email / GitHub link]  
