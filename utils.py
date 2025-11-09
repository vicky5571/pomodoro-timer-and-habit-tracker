import json
import winsound
from config import HABIT_FILE

def load_habits():
    try:
        with open(HABIT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_habits(habits):
    with open(HABIT_FILE, "w") as f:
        json.dump(habits, f, indent=4)

def play_sound():
    try:
        winsound.Beep(1000, 400)
    except:
        pass
