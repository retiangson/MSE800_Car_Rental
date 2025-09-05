
from datetime import datetime, date

def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except Exception as e:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.") from e

def parse_int(s: str) -> int:
    try:
        return int(s)
    except Exception as e:
        raise ValueError("Please enter a valid integer.") from e

def parse_float(s: str) -> float:
    try:
        return float(s)
    except Exception as e:
        raise ValueError("Please enter a valid number.") from e
