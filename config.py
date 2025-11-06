import os
import json

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

HABIT_FILE = os.path.join(DATA_DIR, "habits.json")
CAL_FILE = os.path.join(DATA_DIR, "calendar_log.json")
WEEKLY_FILE = os.path.join(DATA_DIR, "weekly_minutes.json")
POMODORO_LOG = os.path.join(DATA_DIR, "pomodoro_log.txt")

WORK_MINUTES = 25
BREAK_MINUTES = 5

for file_path in [HABIT_FILE, CAL_FILE, WEEKLY_FILE, POMODORO_LOG]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            if file_path.endswith(".txt"):
                f.write("")
            else:
                json.dump({}, f)
