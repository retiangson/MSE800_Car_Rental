from datetime import datetime

class RentalCalculator:
    """Utility class for rental duration and cost calculations."""

    @staticmethod
    def calculate_days(start_date: str, end_date: str | datetime, actual_return: bool = False) -> int:
        """
        Calculate rental duration in days (minimum = 1).
        
        Args:
            start_date (str): Rental start date (YYYY-MM-DD).
            end_date (str | datetime): Rental end date or actual return date.
            actual_return (bool): If True, end_date is a datetime object.
        
        Returns:
            int: Number of days (at least 1).
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")

        if isinstance(end_date, str) and not actual_return:
            end = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end = end_date  # already datetime (actual return)

        return max((end - start).days, 1)

    @staticmethod
    def calculate_cost(base_rate: float, days: int) -> float:
        """
        Calculate total cost given a daily rate and duration.
        
        Args:
            base_rate (float): Daily rental rate.
            days (int): Number of days.
        
        Returns:
            float: Total rental cost.
        """
        return base_rate * days
