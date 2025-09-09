import tkinter as tk
from tkinter import ttk

import calendar
import datetime

class Calendar:
    
    COLOR_SUNDAY_BG = "#F5FF90"
    COLOR_HOLIDAY_BG = "#D6FFB7"
    
    def __init__(self):
        self.root = tk.Tk()
        
        self.current_month = datetime.datetime.now().month
        self.current_month = 10
        self.current_year = datetime.datetime.now().year
        
        self.create_widgets()
        self.update_calendar()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.grid()
        
        self.calendar_frame = ttk.Frame(main_frame)
        self.calendar_frame.grid()
        
            
        self.create_calendar_grid()
            
    def create_calendar_grid(self):
        # Create cells for days
        self.day_cells = []
        # 6 weeks, because day can start on sunday
        for row in range(1, 7):
            week_cells = []
            # 7 days in a week
            for col in range(7):
                cell = tk.Label(self.calendar_frame, text="", font=('Arial', 12),
                            relief='raised', borderwidth=1, width=6, height=3)
                cell.grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), padx=1, pady=1)
                week_cells.append(cell)
            self.day_cells.append(week_cells)
            
    def update_calendar(self):
        for week in self.day_cells:
            for cell in week:
                cell.config(text="", bg='white', fg='black')
        
        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        
        print(month_days)
        
        for week_idx, week in enumerate(month_days):
            if week_idx >= len(self.day_cells):
                break
                
            for day_idx, day in enumerate(week):
                if day == 0:
                    continue # Empty day
                
                cell = self.day_cells[week_idx][day_idx]
                cell.config(text=str(day))
                
                if self.is_sunday(day, self.current_month, self.current_year):
                    cell.config(bg=self.COLOR_SUNDAY_BG, fg='black')
                else:
                    cell.config(bg='white', fg='black')
                
    
    # TODO: Move to separate file          
    def is_sunday(self, day: int, month: int, year: int) -> bool:
        """Preveri, ali je določen dan nedelja"""
        date_obj = datetime.date(year, month, day)
        return date_obj.weekday() == 6  # Nedelja = 6
        
    
    def run(self):
        self.root.mainloop()
        

def main():
    try:
        app = Calendar()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    main()
