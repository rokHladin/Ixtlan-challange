import tkinter as tk
from tkinter import ttk

class Calendar:
    
    def __init__(self):
        self.root = tk.Tk()
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
