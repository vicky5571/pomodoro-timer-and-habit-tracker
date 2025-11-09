import tkinter as tk

from tkinter import ttk
from pomodoro_timer import PomodoroTimer
from habit_tracker import HabitTracker
from mingguan_stats import WeeklyStats

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer and Habit Tracker")
        self.geometry("500x550")

        tab_control = ttk.Notebook(self)
        self.habit_tab = HabitTracker(tab_control)
        self.stats_tab = WeeklyStats(tab_control)
        self.pomodoro_tab = PomodoroTimer(tab_control, self.habit_tab, self.stats_tab)

        tab_control.add(self.pomodoro_tab, text="Pomodoro Timer")
        tab_control.add(self.habit_tab, text="Habit Tracker")
        tab_control.add(self.stats_tab, text="Weekly Stats")
        tab_control.pack(expand=1, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()
