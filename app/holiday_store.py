from tkinter import messagebox


class HolidayStore:
    """
    A class for managing and storing holiday information.
    
    This class handles loading holidays from a text file and provides functionality
    to check if a specific date is a holiday. It supports both yearly recurring
    holidays and one-time holidays for specific years.
    
    Attributes:
        holidays_file (str): Path to the holidays configuration file
        holidays (set): Set of tuples containing holiday information
    """
    
    def __init__(self, holidays_file: str = "../assets/holidays.txt"):
        """
        Initialize the HolidayStore with a holidays file.
        
        Args:
            holidays_file (str): Path to the file containing holiday definitions.
                                Defaults to "../assets/holidays.txt"
        """
        self.holidays_file = holidays_file
        self.holidays = set()
        
        self.load_holidays()
        
    def load_holidays(self):
        """
        Load holidays from the specified file.
        
        Reads the holidays file line by line, parsing each valid holiday entry.
        Displays an error message if the file cannot be read.
        
        File format:
            - Lines starting with '#' are treated as comments
            - Empty lines are ignored
            - Valid entries: "DD.MM|Y" (yearly) or "DD.MM.YYYY|N" (one-time)
        """
        holidays_file = self.holidays_file
        
        try:
            with open(holidays_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        self.parse_holiday_line(line, line_num)
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri branju datoteke s prazniki: {e}")
            
    def parse_holiday_line(self, line: str, line_num: int):
        """
        Parse a single line from the holidays file.
        
        Args:
            line (str): The line to parse
            line_num (int): Line number for error reporting
            
        Expected format:
            - "DD.MM|Y" for yearly recurring holidays
            - "DD.MM.YYYY|N" for one-time holidays
            - Comments after '#' are ignored
            
        The parsed holiday is added to the holidays set as a tuple:
        (day, month, year, is_yearly)
        """
        try:
            # Remove comments
            if '#' in line:
                line = line[:line.index('#')]
            
            parts = line.strip().split('|')
            if len(parts) != 2:
                return
            
            date_part = parts[0].strip()
            repeat_flag = parts[1].strip().upper()
            
            # Parse date
            if len(date_part.split('.')) == 2:  # DD.MM format (repeatable)
                day, month = map(int, date_part.split('.'))
                year = None
            elif len(date_part.split('.')) == 3:  # DD.MM.YYYY format (specific year)
                day, month, year = map(int, date_part.split('.'))
            else:
                return
            
            # Add holiday
            self.holidays.add((day, month, year, repeat_flag == 'Y'))
            
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka v vrstici {line_num}: {line.strip()} - {e}")
            
    def is_holiday(self, day: int, month: int, year: int) -> bool:
        """
        Check if the given date is a holiday.
        
        Args:
            day (int): Day of the month (1-31)
            month (int): Month (1-12)
            year (int): Year (e.g., 2024)
            
        Returns:
            bool: True if the date is a holiday, False otherwise
            
        The method checks both:
        - Yearly recurring holidays (matches day and month)
        - One-time holidays (matches day, month, and year exactly)
        """
        for h_day, h_month, h_year, is_yearly in self.holidays:
            if h_month == month and h_day == day:
                if is_yearly or (h_year and h_year == year):
                    return True
        return False