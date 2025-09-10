import datetime

def is_sunday(day: int, month: int, year: int) -> bool:
    """
    Check if the given date falls on a Sunday.
    
    Args:
        day (int): Day of the month (1-31)
        month (int): Month (1-12)
        year (int): Year (e.g., 2024)
        
    Returns:
        bool: True if the date is a Sunday, False otherwise
        
    Note:
        Uses Python's weekday() method where Monday=0 and Sunday=6
    """
    date_obj = datetime.date(year, month, day)
    return date_obj.weekday() == 6  # Nedelja = 6

def is_today(day: int, month: int, year: int) -> bool:
    """
    Check if the given date is today's date.
    
    Args:
        day (int): Day of the month (1-31)
        month (int): Month (1-12)
        year (int): Year (e.g., 2024)
        
    Returns:
        bool: True if the date matches today's date, False otherwise
        
    Note:
        Compares against the current system date at the time of function call
    """
    date = datetime.datetime.now()
    true_day = date.day
    true_month = date.month
    true_year = date.year
    return day == true_day and month == true_month and year == true_year