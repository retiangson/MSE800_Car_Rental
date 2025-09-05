
def row_to_car_str(row) -> str:
    # row: (id, make, model, year, type, base_rate, status)
    return f"#{row[0]:<3} | {row[1]:<10} {row[2]:<12} | {row[3]} | {row[4]:<8} | ${row[5]:.2f}/day | {row[6]}"

def row_to_customer_str(row) -> str:
    # row: (id, name, email, phone)
    return f"#{row[0]:<3} | {row[1]:<20} | {row[2]:<25} | {row[3]}"

def row_to_rental_str(row) -> str:
    # row: (id, car_id, customer_id, start_date, planned_end_date, returned_date, total_price)
    return f"#{row[0]:<3} | car={row[1]} | cust={row[2]} | start={row[3]} | planned_end={row[4]} | returned={row[5]} | total=${row[6] if row[6] is not None else '—'}"
