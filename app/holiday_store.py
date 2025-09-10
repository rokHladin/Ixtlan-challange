from tkinter import messagebox


class HolidayStore:
    def __init__(self, holidays_file: str = "../assets/holidays.txt"):
        self.holidays_file = holidays_file
        self.holidays = set()
        
        self.load_holidays()
        
    def load_holidays(self):
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
        """Check if the given day is a holiday"""
        for h_day, h_month, h_year, is_yearly in self.holidays:
            if h_month == month and h_day == day:
                if is_yearly or (h_year and h_year == year):
                    return True
        return False