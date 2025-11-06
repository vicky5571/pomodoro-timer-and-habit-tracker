import json
import os
from datetime import datetime

WEEKLY_FILE = "weekly_minutes.json"

# memastikan file ada
if not os.path.exists(WEEKLY_FILE):
    with open(WEEKLY_FILE, "w") as f:
        json.dump({}, f)

def add_session(minutes):
    """Tambah menit Pomodoro ke hari ini"""
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        with open(WEEKLY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[today] = data.get(today, 0) + minutes

    with open(WEEKLY_FILE, "w") as f:
        json.dump(data, f, indent=4)
