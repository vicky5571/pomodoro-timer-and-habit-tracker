import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils import load_habits, save_habits
from delete_for_habit import delete
from edit_habit_tracker import edit
from calender_log import add_calendar_log, CalendarMatrix

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

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.add_button = ttk.Button(btn_frame, text="Add Habit", command=self.add_habit)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = ttk.Button(btn_frame, text="Edit Habit", command=self.edit_habit)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.done_button = ttk.Button(btn_frame, text="Mark Done", command=self.mark_done)
        self.done_button.grid(row=0, column=2, padx=5)

        self.reset_button = ttk.Button(btn_frame, text="Reset Day", command=self.reset_habits)
        self.reset_button.grid(row=0, column=3, padx=5)

        self.delete_button = ttk.Button(btn_frame, text="Delete Habit", command=self.delete_habit)
        self.delete_button.grid(row=0, column=4, padx=5)

        self.calendar_button = ttk.Button(self, text="Calendar Log", command=self.open_calendar)
        self.calendar_button.pack(side="left", padx=10, pady=10)

    def refresh_list(self):
        self.habit_listbox.delete(0, "end")
        for name, data in self.habits.items():
            status = "✅" if data.get("done_today") else "❌"
            count = data.get("count", 0)
            self.habit_listbox.insert("end", f"{name}  [{status}] (Total: {count})")

    def add_habit(self):
        new_habit = simpledialog.askstring("Add Habit", "Enter new habit name:")
        if new_habit:
            if new_habit in self.habits:
                messagebox.showwarning("Duplicate", "Habit already exists!")
                return
            self.habits[new_habit] = {"done_today": False, "count": 0}
            save_habits(self.habits)
            self.refresh_list()

    def edit_habit(self):
        edit(self)

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

    def delete_habit(self):
        delete(self)

    def increment_focus_habit(self):
        if "Fokus Belajar" in self.habits:
            self.habits["Fokus Belajar"]["count"] += 1
            self.habits["Fokus Belajar"]["done_today"] = True
            save_habits(self.habits)
            self.refresh_list()

    def open_calendar(self):
        habit_names = list(self.habits.keys())
        CalendarMatrix(self, habit_names)
