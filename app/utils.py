import datetime

def is_sunday(day: int, month: int, year: int) -> bool:
    """Check if the given day is a Sunday"""
    date_obj = datetime.date(year, month, day)
    return date_obj.weekday() == 6  # Nedelja = 6

def is_today(day: int, month: int, year: int) -> bool:
    date = datetime.datetime.now()
    true_day = date.day
    true_month = date.month
    true_year = date.year
    return day == true_day and month == true_month and year == true_year