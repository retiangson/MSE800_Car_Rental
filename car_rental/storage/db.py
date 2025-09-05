
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "car_rental.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('manager','employee'))
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            type TEXT NOT NULL,
            base_rate REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'available',
            date_created TEXT DEFAULT CURRENT_TIMESTAMP,
            date_updated TEXT,
            created_by INTEGER,
            updated_by INTEGER,
            FOREIGN KEY(created_by) REFERENCES users(id),
            FOREIGN KEY(updated_by) REFERENCES users(id)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rentals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            planned_end_date TEXT,
            returned_date TEXT,
            total_price REAL,
            date_created TEXT DEFAULT CURRENT_TIMESTAMP,
            date_updated TEXT,
            created_by INTEGER,
            updated_by INTEGER,
            FOREIGN KEY(car_id) REFERENCES cars(id),
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(created_by) REFERENCES users(id),
            FOREIGN KEY(updated_by) REFERENCES users(id)
        );
    ''')
    conn.commit()
    conn.close()

def init_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0]==0:
        cur.execute("INSERT INTO users(username,password,role) VALUES (?,?,?);",("admin","admin","manager"))
        cur.execute("INSERT INTO users(username,password,role) VALUES (?,?,?);",("employee","employee","employee"))
    conn.commit()
    conn.close()
