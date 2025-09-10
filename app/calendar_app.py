import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import calendar
import datetime
from typing import List

from utils import is_sunday, is_today

from holiday_store import HolidayStore

class Calendar:
    """    
    This class creates a fully-featured calendar interface with month navigation,
    date jumping, and visual highlighting for special dates (holidays, weekends, today).
    The interface uses a modern color palette and responsive design.
    
    Attributes:        
        root (tk.Tk): Main tkinter window
        current_month (int): Currently displayed month (1-12)
        current_year (int): Currently displayed year
        holiday_store (HolidayStore): Holiday data management instance
        day_names (List[str]): Slovenian day names for calendar headers
        month_names (List[str]): Slovenian month names for navigation
    """
    
    # Color palette
    COLOR_PRIMARY = "#6366F1"        # Modern indigo
    COLOR_PRIMARY_LIGHT = "#8B5CF6"  # Light purple
    COLOR_SECONDARY = "#06B6D4"      # Cyan
    COLOR_BACKGROUND = "#F8FAFC"     # Light gray background
    COLOR_SURFACE = "#FFFFFF"        # White surface
    COLOR_SURFACE_VARIANT = "#F1F5F9" # Light gray variant
    COLOR_ON_SURFACE = "#1E293B"     # Dark text
    COLOR_ON_SURFACE_VARIANT = "#64748B" # Gray text
    COLOR_SUNDAY_BG = "#FEF3C7"      # Soft yellow
    COLOR_HOLIDAY_BG = "#FEE2E2"     # Soft red
    COLOR_TODAY_BG = "#DBEAFE"       # Soft blue
    COLOR_HOVER = "#E2E8F0"          # Light hover
    COLOR_SHADOW = "#E2E8F0"         # Shadow color
    
    def __init__(self):
        """
        Initialize the Calendar application.
        
        Sets up the main window, initializes date variables, loads holiday data,
        defines localized day/month names, creates the UI widgets, and displays
        the current month's calendar.
        """
        self.root = tk.Tk()
        self.setup_window()
        
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        
        self.holiday_store = HolidayStore(holidays_file="./assets/holidays.txt")
        
        self.day_names:List[str] = ["Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned"]
        
        self.month_names = [
            "Januar", "Februar", "Marec", "April", "Maj", "Junij",
            "Julij", "Avgust", "September", "Oktober", "November", "December"
        ]
        
        self.create_widgets()
        self.update_calendar()
        
    def setup_window(self):
        """
        Configure the main application window and ttk styles.
        
        Sets up window properties (title, size, position), configures ttk themes
        and styles for various UI components including buttons, labels, entries,
        and comboboxes. Also defines hover effects and state-based styling.
        """
        self.root.title("Koledar")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg=self.COLOR_BACKGROUND)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (8000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for ttk widgets
        style.configure('Modern.TFrame', background=self.COLOR_SURFACE)
        style.configure('Nav.TFrame', background=self.COLOR_SURFACE_VARIANT, 
                        relief='flat', borderwidth=1)
        
        # Enhanced label styling
        style.configure('Modern.TLabel', background=self.COLOR_SURFACE, 
                        foreground=self.COLOR_ON_SURFACE, font=('Segoe UI', 11))
        style.configure('Nav.TLabel', background=self.COLOR_SURFACE_VARIANT, 
                        foreground=self.COLOR_ON_SURFACE, font=('Segoe UI', 11, 'normal'))
        style.configure('Title.TLabel', background=self.COLOR_SURFACE,
                        foreground=self.COLOR_ON_SURFACE, font=('Segoe UI', 20, 'bold'))
        style.configure('NavTitle.TLabel', background=self.COLOR_SURFACE_VARIANT,
                        foreground=self.COLOR_ON_SURFACE, font=('Segoe UI', 18, 'bold'))
        style.configure('Header.TLabel', background=self.COLOR_PRIMARY,
                        foreground='white', font=('Segoe UI', 12, 'bold'))
        
        # Enhanced button styling with rounded appearance
        style.configure('Modern.TButton', 
                        font=('Segoe UI', 10),
                        borderwidth=1,
                        focuscolor='none',
                        padding=(12, 8),
                        relief='flat')
        style.configure('Primary.TButton', 
                        font=('Segoe UI', 10, 'bold'),
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(16, 10),
                        relief='flat')
        
        # Enhanced input styling
        style.configure('Modern.TCombobox', 
                        font=('Segoe UI', 11),
                        fieldbackground=self.COLOR_SURFACE,
                        borderwidth=2,
                        insertwidth=2,
                        padding=(8, 6))
        style.configure('Modern.TEntry', 
                        font=('Segoe UI', 11),
                        fieldbackground=self.COLOR_SURFACE,
                        borderwidth=2,
                        insertwidth=2,
                        padding=(8, 6))
        
        # Enhanced button hover and state effects
        style.map('Modern.TButton',
                    background=[('!active', self.COLOR_SURFACE_VARIANT),
                                ('active', self.COLOR_HOVER),
                                ('pressed', self.COLOR_PRIMARY_LIGHT)],
                    bordercolor=[('!active', self.COLOR_ON_SURFACE_VARIANT),
                            ('active', self.COLOR_PRIMARY),
                            ('pressed', self.COLOR_PRIMARY)])
        style.map('Primary.TButton',
                    background=[('!active', self.COLOR_PRIMARY),
                            ('active', self.COLOR_PRIMARY_LIGHT),
                            ('pressed', self.COLOR_SECONDARY)],
                    relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Enhanced input field effects
        style.map('Modern.TCombobox',
                    fieldbackground=[('!active', self.COLOR_SURFACE),
                                ('active', self.COLOR_SURFACE)],
                    bordercolor=[('!active', self.COLOR_ON_SURFACE_VARIANT),
                            ('active', self.COLOR_PRIMARY),
                            ('focus', self.COLOR_PRIMARY)])
        style.map('Modern.TEntry',
                    fieldbackground=[('!active', self.COLOR_SURFACE),
                                ('active', self.COLOR_SURFACE)],
                    bordercolor=[('!active', self.COLOR_ON_SURFACE_VARIANT),
                            ('active', self.COLOR_PRIMARY),
                            ('focus', self.COLOR_PRIMARY)])
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
    def create_widgets(self):
        """
        Create and configure all UI widgets for the calendar application.
        
        Builds the complete UI structure including:
        - Main container frame
        - Navigation controls (month/year selection, date jump)
        - Calendar title display
        - Calendar grid container
        
        Uses ttk widgets with custom styling for a modern appearance.
        """
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Navigation container with card-like appearance
        nav_container = ttk.Frame(main_frame, style='Nav.TFrame', padding="16")
        nav_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 25))
        nav_container.columnconfigure(1, weight=1)
        
        # Controls section
        controls_frame = ttk.Frame(nav_container, style='Nav.TFrame')
        controls_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 12))
        controls_frame.columnconfigure(2, weight=1)
        
        # Month and Year controls (left side)
        month_year_frame = ttk.Frame(controls_frame, style='Nav.TFrame')
        month_year_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Month selection
        ttk.Label(month_year_frame, text="Mesec:", style='Nav.TLabel').grid(row=0, column=0, padx=(0, 8), pady=(0, 2))
        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(month_year_frame, textvariable=self.month_var,
                                    values=self.month_names, state="readonly", 
                                    width=13, style='Modern.TCombobox')
        self.month_combo.grid(row=0, column=1, padx=(0, 20), pady=(0, 2))
        self.month_combo.bind('<<ComboboxSelected>>', self.on_month_changed)

        # Year input
        ttk.Label(month_year_frame, text="Leto:", style='Nav.TLabel').grid(row=0, column=2, padx=(0, 8), pady=(0, 2))
        self.year_var = tk.IntVar()
        self.year_entry = ttk.Entry(month_year_frame, textvariable=self.year_var, 
                                    width=8, style='Modern.TEntry', justify='center')
        self.year_entry.grid(row=0, column=3, pady=(0, 2))
        self.year_entry.bind('<Return>', self.on_year_changed)
        self.year_entry.bind('<FocusOut>', self.on_year_changed)

        # Date jump controls (right side)
        jump_frame = ttk.Frame(controls_frame, style='Nav.TFrame')
        jump_frame.grid(row=0, column=3, sticky=tk.E)
        
        # Jump to date
        ttk.Label(jump_frame, text="Skoči na:", style='Nav.TLabel').grid(row=0, column=1, padx=(0, 8), pady=(0, 2))
        self.jump_date_var = tk.StringVar()
        self.jump_date_entry = ttk.Entry(jump_frame, textvariable=self.jump_date_var, 
                                        width=11, style='Modern.TEntry', justify='center')
        self.jump_date_entry.grid(row=0, column=2, padx=(0, 12), pady=(0, 2))
        self.jump_date_entry.bind('<Return>', self.jump_to_date)
        self.jump_date_entry.insert(0, "DD.MM.YYYY")
        self.jump_date_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e))
        self.jump_date_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e))
        
        jump_button = ttk.Button(jump_frame, text="Pojdi", command=self.jump_to_date,
                                style='Primary.TButton', cursor='hand2')
        jump_button.grid(row=0, column=3, pady=(0, 2))
        
        # Title section
        title_section = ttk.Frame(nav_container, style='Nav.TFrame')
        title_section.grid(row=1, column=0, columnspan=2, pady=(12, 0))
        title_section.columnconfigure(1, weight=1)
        
        
        self.title_var = tk.StringVar()
        title_label = ttk.Label(title_section, textvariable=self.title_var, 
                                style='NavTitle.TLabel')
        title_label.grid(row=0, column=1, padx=10)
        
        
        # Calendar container
        calendar_container = ttk.Frame(main_frame, style='Modern.TFrame')
        calendar_container.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        calendar_container.columnconfigure(0, weight=1)
        calendar_container.rowconfigure(0, weight=1)
        
        # Shadow frame (simulated)
        shadow_frame = tk.Frame(calendar_container, bg=self.COLOR_SHADOW, height=2)
        shadow_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(2, 0))
        
        self.calendar_frame = tk.Frame(calendar_container, bg=self.COLOR_SURFACE, 
                                        relief='flat', borderwidth=0)
        self.calendar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure calendar grid
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(7):  # Maximum 7 rows (headers + 6 weeks)
            self.calendar_frame.rowconfigure(i, weight=1)
    
        self.create_calendar_grid()
        
    def clear_placeholder(self, event):
        """
        Clear placeholder text when entry widget receives focus.
        
        Args:
            event: tkinter event object containing the widget that received focus
        """
        if event.widget.get() == "DD.MM.YYYY":
            event.widget.delete(0, tk.END)
            
    def restore_placeholder(self, event):
        """
        Restore placeholder text if entry widget is empty when losing focus.
        
        Args:
            event: tkinter event object containing the widget that lost focus
        """
        if not event.widget.get():
            event.widget.insert(0, "DD.MM.YYYY")
        
    def on_month_changed(self, event=None):
        """
        Handle month selection change from the combobox.
        
        Updates the current_month attribute based on the selected month name
        and refreshes the calendar display.
        
        Args:
            event: tkinter event object (optional, defaults to None)
        """
        try:
            month_name = self.month_var.get()
            if month_name in self.month_names:
                self.current_month = self.month_names.index(month_name) + 1
                self.update_calendar()
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri spremembi meseca: {e}")
            
    def on_year_changed(self, event=None):
        """
        Handle year input change from the entry widget.
        
        Updates the current_year attribute based on the entered year value
        and refreshes the calendar display.
        
        Args:
            event: tkinter event object (optional, defaults to None)
        """
        try:
            year = self.year_var.get()
            if year:
                self.current_year = year
                self.update_calendar()
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri spremembi leta: {e}")
            
    def jump_to_date(self, event=None):
        """
        Jump to a specific date entered by the user.
        
        Parses date input in DD.MM.YYYY format, validates the date,
        and navigates to the corresponding month and year.
        
        Args:
            event: tkinter event object (optional, defaults to None)
            
        Raises:
            ValueError: If the date format is invalid or date doesn't exist
        """
        try:
            date_str = self.jump_date_var.get().strip()
            if not date_str or date_str == "DD.MM.YYYY":
                return
            
            # Parse data in format DD.MM.YYYY
            parts = date_str.split('.')
            if len(parts) != 3:
                messagebox.showerror("Napaka", "Datum mora biti v formatu DD.MM.YYYY")
                return
            
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
            
            # Check if the date is valid
            datetime.date(year, month, day)  # If date is invalid, this will raise an exception
            
            # Set new month and year
            self.current_month = month
            self.current_year = year
            self.update_calendar()
            
            # Clear the jump date field and restore placeholder
            self.jump_date_var.set("DD.MM.YYYY")
            
        except ValueError as e:
            messagebox.showerror("Napaka", f"Neveljaven datum: {e}")
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri skoku na datum: {e}")

            
    def create_calendar_grid(self):
        """
        Create the calendar grid layout with day headers and date cells.
        
        Creates:
        - Row of day name headers (Pon, Tor, Sre, etc.)
        - 6x7 grid of date cells for displaying days (6 weeks max)
        
        All cells are initialized as empty labels that will be populated
        by update_calendar().
        """
        
        self.day_headers = []
        for col, day_name in enumerate(self.day_names):
            header = tk.Label(self.calendar_frame, text=day_name, 
                            font=('Segoe UI', 14, 'bold'),
                            bg=self.COLOR_PRIMARY, fg='white',
                            relief='flat', borderwidth=0, height=3)
            header.grid(row=0, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), 
                        padx=1, pady=(0, 2))
            self.day_headers.append(header)
        
        # Create cells for days
        self.day_cells = []
        # 6 weeks, because day can start on sunday
        for row in range(1, 7):
            week_cells = []
            # 7 days in a week
            for col in range(7):
                cell = tk.Label(self.calendar_frame, text="", 
                                font=('Segoe UI', 13),
                                bg=self.COLOR_SURFACE, fg=self.COLOR_ON_SURFACE,
                                relief='flat', borderwidth=0, width=8, height=4,
                                )
                cell.grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), 
                            padx=1, pady=1)
                
                week_cells.append(cell)
            self.day_cells.append(week_cells)
        
    def update_calendar(self):
        """
        Update the calendar display with current month and year data.
        
        Refreshes the calendar by:
        - Updating month/year controls with current values
        - Updating the title display
        - Clearing all existing date cells
        - Populating cells with current month's days
        - Applying appropriate styling based on date type:
          * Today's date: highlighted in blue
          * Holidays: highlighted in red
          * Sundays: highlighted in yellow
          * Regular days: default styling
        """
        
        self.month_var.set(self.month_names[self.current_month - 1])
        self.year_var.set(self.current_year)
        
        # Update title
        self.title_var.set(f"{self.month_names[self.current_month - 1]} {self.current_year}")
        
        # Clear all cells
        for week in self.day_cells:
            for cell in week:
                cell.config(text="", bg=self.COLOR_SURFACE, 
                            fg=self.COLOR_ON_SURFACE)
        
        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        
        for week_idx, week in enumerate(month_days):
            if week_idx >= len(self.day_cells):
                break
                
            for day_idx, day in enumerate(week):
                if day == 0:
                    continue # Empty day
                
                cell = self.day_cells[week_idx][day_idx]
                cell.config(text=str(day))
                
                # Color cells based on the day
                if is_today(day, self.current_month, self.current_year):
                    cell.config(bg=self.COLOR_TODAY_BG, 
                                fg=self.COLOR_ON_SURFACE, 
                                font=('Segoe UI', 13, 'bold'))
                elif self.holiday_store.is_holiday(day, self.current_month, self.current_year):
                    cell.config(bg=self.COLOR_HOLIDAY_BG, 
                                fg=self.COLOR_ON_SURFACE,
                                font=('Segoe UI', 13, 'bold'))
                elif is_sunday(day, self.current_month, self.current_year):
                    cell.config(bg=self.COLOR_SUNDAY_BG, 
                                fg=self.COLOR_ON_SURFACE_VARIANT,
                                font=('Segoe UI', 13))
                else:
                    cell.config(bg=self.COLOR_SURFACE, 
                                fg=self.COLOR_ON_SURFACE,
                                font=('Segoe UI', 13))
                    
    def run(self):
        """
        Start the main application event loop.
        
        Begins the tkinter mainloop to handle user interactions
        and keep the application running.
        """
        self.root.mainloop()
        

def main():
    """
    Main entry point for the calendar application.
    
    Creates and runs a Calendar instance, with basic error handling
    to catch and display any startup exceptions.
    """
    try:
        app = Calendar()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    main()
