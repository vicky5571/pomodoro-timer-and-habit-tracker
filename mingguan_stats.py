import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from config import POMODORO_LOG

MINUTES_FILE = "weekly_minutes.json"


# ✅ Helper: load JSON
def load_minutes():
    if not os.path.exists(MINUTES_FILE):
        with open(MINUTES_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(MINUTES_FILE, "r") as f:
        return json.load(f)

def save_minutes(data):
    with open(MINUTES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_session(minutes):
    data = load_minutes()

    day_key = datetime.now().strftime("%Y-%m-%d")

    if day_key not in data:
        data[day_key] = 0

    data[day_key] += minutes
    save_minutes(data)

def load_activity():
    return load_minutes()


# ambil data 7 hari terakhir
def get_last7():
    raw = load_activity()
    today = datetime.now().date()
    days = {}

    for i in range(7):
        d = today - timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        days[key] = raw.get(key, 0)

    return dict(sorted(days.items()))


# tampilkan grafik
def show_graph():
    data = get_last7()
    dates = list(data.keys())
    values = list(data.values())

    plt.figure()
    plt.plot(dates, values, marker="o")
    plt.title("Weekly Productivity Stats")
    plt.xlabel("Date")
    plt.ylabel("Total Minutes (Pomodoro)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#  Window standalone
def open_weekly_stats(root):
    win = tk.Toplevel(root)
    win.title("Weekly Stats")
    win.geometry("420x360")

    label = ttk.Label(win, text="Weekly Productivity Statistics", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    frame = ttk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("Date", "Minutes"), show="headings", height=8)
    tree.heading("Date", text="Date")
    tree.heading("Minutes", text="Minutes")

    data = get_last7()
    for d, m in data.items():
        tree.insert("", "end", values=(d, m))

    tree.pack(fill="both", expand=True)

    info = ttk.Label(
        win,
        text="📌 Menampilkan total menit hasil pomodoro selama 7 hari terakhir.",
        wraplength=380,
        justify="left"
    )
    info.pack(pady=10)

    btn = ttk.Button(win, text="Tampilkan Grafik", command=show_graph)
    btn.pack(pady=10)


# Class versi embed
class WeeklyStats(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = ttk.Label(self, text="Weekly Productivity Statistics", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("Date", "Minutes"), show="headings", height=8)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Minutes", text="Minutes")
        self.tree.pack(fill="both", expand=True)

        self.refresh()

        btn = ttk.Button(self, text="📊 Show Graph", command=show_graph)
        btn.pack(pady=10)

    def refresh(self):
        """Reload isi treeview dari JSON"""
        data = get_last7()

        # hapus rows lama
        for row in self.tree.get_children():
            self.tree.delete(row)

        # tambah rows baru
        for d, m in data.items():
            self.tree.insert("", "end", values=(d, m))
