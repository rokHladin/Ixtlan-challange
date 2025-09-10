import sys

sys.path.append("./app")


from app.calendar_app import Calendar

try:
    app = Calendar()
    app.run()
except Exception as e:
    print(f"Error: {e}")