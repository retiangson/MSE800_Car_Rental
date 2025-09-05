
from datetime import date
from typing import Optional, List, Tuple
from .db import get_connection

def add_car(make,model,year,vtype,base_rate,user_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("INSERT INTO cars(make,model,year,type,base_rate,status,created_by) VALUES (?,?,?,?,?,'available',?);",
                (make,model,year,vtype,base_rate,user_id))
    conn.commit(); cid=cur.lastrowid; conn.close(); return cid

def update_car(car_id,make=None,model=None,year=None,vtype=None,base_rate=None,user_id=None):
    fields,vals=[],[]
    if make is not None: fields.append("make=?"); vals.append(make)
    if model is not None: fields.append("model=?"); vals.append(model)
    if year is not None: fields.append("year=?"); vals.append(year)
    if vtype is not None: fields.append("type=?"); vals.append(vtype)
    if base_rate is not None: fields.append("base_rate=?"); vals.append(base_rate)
    if user_id is not None:
        fields.append("date_updated=CURRENT_TIMESTAMP")
        fields.append("updated_by=?"); vals.append(user_id)
    vals.append(car_id)
    conn=get_connection(); cur=conn.cursor()
    cur.execute(f"UPDATE cars SET {', '.join(fields)} WHERE id=?;",vals)
    conn.commit(); conn.close()

def add_customer(name,email,phone):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("INSERT INTO customers(name,email,phone) VALUES (?,?,?);",(name,email,phone))
    conn.commit(); cid=cur.lastrowid; conn.close(); return cid

def list_customers()->List[Tuple]:
    conn=get_connection(); cur=conn.cursor()
    cur.execute("SELECT id,name,email,phone FROM customers ORDER BY id;")
    rows=cur.fetchall(); conn.close(); return rows

def get_customer_by_email(email)->Optional[Tuple]:
    conn=get_connection(); cur=conn.cursor()
    cur.execute("SELECT id,name,email,phone FROM customers WHERE email=?;",(email,))
    row=cur.fetchone(); conn.close(); return row

def get_car(car_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("SELECT id,make,model,year,type,base_rate,status FROM cars WHERE id=?;",(car_id,))
    row=cur.fetchone(); conn.close(); return row

def set_car_status(car_id,status):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("UPDATE cars SET status=?,date_updated=CURRENT_TIMESTAMP WHERE id=?;",(status,car_id))
    conn.commit(); conn.close()

def create_rental(car_id,customer_id,start_date,planned_end_date,user_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("INSERT INTO rentals(car_id,customer_id,start_date,planned_end_date,created_by) VALUES (?,?,?,?,?);",
                (car_id,customer_id,start_date.isoformat(),planned_end_date.isoformat() if planned_end_date else None,user_id))
    conn.commit(); rid=cur.lastrowid; conn.close(); return rid

def return_rental(rental_id,returned_date,total_price,user_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("UPDATE rentals SET returned_date=?,total_price=?,date_updated=CURRENT_TIMESTAMP,updated_by=? WHERE id=?;",
                (returned_date.isoformat(),total_price,user_id,rental_id))
    conn.commit(); conn.close()

def get_active_rental_by_car(car_id):
    conn=get_connection(); cur=conn.cursor()
    cur.execute("SELECT id,car_id,customer_id,start_date,planned_end_date FROM rentals WHERE car_id=? AND returned_date IS NULL;",(car_id,))
    row=cur.fetchone(); conn.close(); return row

def list_rentals(active_only=False):
    conn=get_connection(); cur=conn.cursor()
    if active_only:
        cur.execute("SELECT id,car_id,customer_id,start_date,planned_end_date,returned_date,total_price FROM rentals WHERE returned_date IS NULL ORDER BY id;")
    else:
        cur.execute("SELECT id,car_id,customer_id,start_date,planned_end_date,returned_date,total_price FROM rentals ORDER BY id;")
    rows=cur.fetchall(); conn.close(); return rows

def list_cars(include_unavailable=True):
    conn=get_connection(); cur=conn.cursor()
    if include_unavailable:
        cur.execute("SELECT id,make,model,year,type,base_rate,status FROM cars ORDER BY id;")
    else:
        cur.execute("SELECT id,make,model,year,type,base_rate,status FROM cars WHERE status='available' ORDER BY id;")
    rows=cur.fetchall(); conn.close(); return rows
