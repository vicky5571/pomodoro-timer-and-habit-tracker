import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import json
import os
from datetime import datetime
from calendar_log import add_calendar_log, CalendarMatrix
import winsound  # gunakan di Windows, bisa diganti playsound di OS lain

# ===============================
# === FILE DAN KONSTANTA DATA ===
# ===============================

DATA_DIR = "data"
HABIT_FILE = os.path.join(DATA_DIR, "habits.json")
POMODORO_LOG = os.path.join(DATA_DIR, "pomodoro_log.txt")

WORK_MINUTES = 25
BREAK_MINUTES = 5

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(HABIT_FILE):
    with open(HABIT_FILE, "w") as f:
        json.dump({}, f)


# ===============================
# === FUNGSI BANTUAN ===
# ===============================

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


# ===============================
# === CLASS POMODORO TIMER ===
# ===============================

class PomodoroTimer(ttk.Frame):
    def __init__(self, parent, habit_tracker):
        super().__init__(parent)
        self.parent = parent
        self.habit_tracker = habit_tracker

        self.is_running = False
        self.is_work_session = True
        self.time_left = WORK_MINUTES * 60
        self.session_count = 0
        self.timer_thread = None

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Pomodoro Timer", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=10)

        self.time_display = ttk.Label(self, text=self.format_time(self.time_left), font=("Helvetica", 36))
        self.time_display.pack(pady=20)

        self.status_label = ttk.Label(self, text="Status: Work Time", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.start_button = ttk.Button(self, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.pause_button = ttk.Button(self, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side="left", padx=10, pady=10)

        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10, pady=10)

        self.log_label = ttk.Label(self, text="Session Log:", font=("Helvetica", 10, "bold"))
        self.log_label.pack(pady=10)

        self.log_box = tk.Text(self, width=45, height=8, state="disabled")
        self.log_box.pack()

    def format_time(self, seconds):
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02}:{sec:02}"

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

    def run_timer(self):
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.update_display()

        if self.is_running and self.time_left == 0:
            play_sound()
            self.session_done()

    def pause_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.is_work_session = True
        self.time_left = WORK_MINUTES * 60
        self.status_label.config(text="Status: Work Time")
        self.update_display()

    def session_done(self):
        self.is_running = False
        self.session_count += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log ke file
        with open(POMODORO_LOG, "a") as f:
            f.write(f"[{now}] Session {self.session_count}: {'Work' if self.is_work_session else 'Break'} done\n")

        # Update di GUI
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{now}] Session {self.session_count} finished ({'Work' if self.is_work_session else 'Break'})\n")
        self.log_box.config(state="disabled")
        self.log_box.see("end")

        # Tambahkan poin ke habit tertentu
        if self.is_work_session:
            self.habit_tracker.increment_focus_habit()

        # Ganti mode
        self.is_work_session = not self.is_work_session
        self.time_left = BREAK_MINUTES * 60 if not self.is_work_session else WORK_MINUTES * 60
        self.status_label.config(text=f"Status: {'Break Time' if not self.is_work_session else 'Work Time'}")
        self.update_display()

    def update_display(self):
        self.time_display.config(text=self.format_time(self.time_left))


# ===============================
# === CLASS HABIT TRACKER ===
# ===============================

class HabitTracker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.habits = load_habits()
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Habit Tracker", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=10)

        self.habit_listbox = tk.Listbox(self, width=40, height=10)
        self.habit_listbox.pack(pady=5)
        self.refresh_list()

        self.add_button = ttk.Button(self, text="Add Habit", command=self.add_habit)
        self.add_button.pack(side="left", padx=10, pady=10)

        self.done_button = ttk.Button(self, text="Mark Done", command=self.mark_done)
        self.done_button.pack(side="left", padx=10, pady=10)

        self.reset_button = ttk.Button(self, text="Reset Day", command=self.reset_habits)
        self.reset_button.pack(side="left", padx=10, pady=10)

        self.calendar_button = ttk.Button(self, text="Calendar Log", command=self.open_calendar)
        self.calendar_button.pack(side="left", padx=10, pady=10)


    def refresh_list(self):
        self.habit_listbox.delete(0, "end")
        for name, data in self.habits.items():
            status = "✅" if data.get("done_today") else "❌"
            self.habit_listbox.insert("end", f"{name}  [{status}]")

    def add_habit(self):
        new_habit = simpledialog.askstring("Add Habit", "Enter new habit name:")
        if new_habit:
            self.habits[new_habit] = {"done_today": False, "count": 0}
            save_habits(self.habits)
            self.refresh_list()

    def mark_done(self):
        selected = self.habit_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a habit first!")
            return

        habit_name = list(self.habits.keys())[selected[0]]
        self.habits[habit_name]["done_today"] = True
        self.habits[habit_name]["count"] += 1
        save_habits(self.habits)
        add_calendar_log(habit_name)
        self.refresh_list()


    def reset_habits(self):
        for h in self.habits:
            self.habits[h]["done_today"] = False
        save_habits(self.habits)
        self.refresh_list()

    def increment_focus_habit(self):
        # Tambah poin ke habit "Fokus Belajar" kalau ada
        if "Fokus Belajar" in self.habits:
            self.habits["Fokus Belajar"]["count"] += 1
            self.habits["Fokus Belajar"]["done_today"] = True
            save_habits(self.habits)
            self.refresh_list()
    
    def open_calendar(self):
        habit_names = list(self.habits.keys())
        CalendarMatrix(self, habit_names)


# ===============================
# === MAIN WINDOW ===
# ===============================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer and Habit Tracker")
        self.geometry("500x500")

        tab_control = ttk.Notebook(self)
        self.habit_tab = HabitTracker(tab_control)
        self.pomodoro_tab = PomodoroTimer(tab_control, self.habit_tab)

        tab_control.add(self.pomodoro_tab, text="Pomodoro Timer")
        tab_control.add(self.habit_tab, text="Habit Tracker")
        tab_control.pack(expand=1, fill="both")


# ===============================
# === ENTRY POINT ===
# ===============================

if __name__ == "__main__":
    app = App()
    app.mainloop()