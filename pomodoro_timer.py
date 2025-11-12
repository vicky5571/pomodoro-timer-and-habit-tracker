import time
import threading
from datetime import datetime
import tkinter as tk
from set_timer import timer
from tkinter import ttk, messagebox, simpledialog
from stats_log import add_session
from config import POMODORO_LOG, WORK_MINUTES, BREAK_MINUTES
from utils import play_sound
from exit_button import add_exit_button


class PomodoroTimer(ttk.Frame):
    def __init__(self, parent, habit_tracker, stats_tab):
        super().__init__(parent)
        self.parent = parent
        self.habit_tracker = habit_tracker
        self.stats_tab = stats_tab 

        self.work_minutes = WORK_MINUTES
        self.break_minutes = BREAK_MINUTES
        self.is_running = False
        self.is_work_session = True
        self.time_left = self.work_minutes * 60
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

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_button = ttk.Button(btn_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(btn_frame, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = ttk.Button(btn_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.settime_button = ttk.Button(btn_frame, text="Set Time", command=self.set_time)
        self.settime_button.grid(row=0, column=3, padx=5)

        self.log_label = ttk.Label(self, text="Session Log:", font=("Helvetica", 10, "bold"))
        self.log_label.pack(pady=10)

        self.log_box = tk.Text(self, width=45, height=8, state="disabled")
        self.log_box.pack()

        exit_frame = add_exit_button(self)
        exit_frame.pack(pady=10)

    def format_time(self, seconds):
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02}:{sec:02}"

    def start_timer(self):
        if not self.is_running:
            self.original_time = self.time_left   
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
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
        self.time_left = self.work_minutes * 60
        self.status_label.config(text="Status: Work Time")
        self.update_display()

    def set_time(self):
        timer(self)

    def session_done(self):
        self.is_running = False
        self.session_count += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Hitung menit kerja sebenarnya lalu log
        if self.is_work_session:
            minutes_done = (self.original_time - self.time_left) // 60
            if minutes_done <= 0:
                minutes_done = 1
            add_session(minutes_done)
            self.stats_tab.refresh()

        # Log ke file
        with open(POMODORO_LOG, "a") as f:
            f.write(f"[{now}] Session {self.session_count}: {'Work' if self.is_work_session else 'Break'} done\n")

        # Update GUI
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{now}] Session {self.session_count} finished ({'Work' if self.is_work_session else 'Break'})\n")
        self.log_box.config(state="disabled")
        self.log_box.see("end")

        # toggle mode
        self.is_work_session = not self.is_work_session
        self.time_left = self.break_minutes * 60 if not self.is_work_session else self.work_minutes * 60
        self.status_label.config(text=f"Status: {'Break Time' if not self.is_work_session else 'Work Time'}")
        self.update_display()

  
    def update_display(self):
        self.time_display.config(text=self.format_time(self.time_left))
