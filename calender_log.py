import os
import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
from config import CAL_FILE

def load_calendar_log():
    try:
        with open(CAL_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_calendar_log(data):
    with open(CAL_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_calendar_log(habit_name, date=None):
    """Tambah habit per tanggal"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    data = load_calendar_log()
    if date not in data:
        data[date] = []

    if habit_name not in data[date]:
        data[date].append(habit_name)

    save_calendar_log(data)



# ========================
#   MAIN CLASS
# ========================
class CalendarMatrix(tk.Toplevel):
    """Tabel Log Bulanan"""

    def __init__(self, parent, habit_names: list):
        super().__init__(parent)
        self.title("Monthly Habit Calendar Log")
        self.geometry("1000x600")

        self.habit_names = habit_names
        self.year = datetime.now().year
        self.month = datetime.now().month

        self.data = load_calendar_log()
        self.configure(bg="#E8F1FF")

        self.create_widgets()
        self.render_table()


    def create_widgets(self):

        title = ttk.Label(
            self,
            text="Calendar Log",
            font=("Helvetica", 18, "bold"),
            foreground="#0F4C75",
            background="#E8F1FF"
        )
        title.pack(pady=10)

        nav = ttk.Frame(self)
        nav.pack()

        ttk.Button(nav, text="<", width=3, command=self.prev_month).grid(row=0, column=0)
        self.month_label = ttk.Label(nav, text="", font=("Helvetica", 12))
        self.month_label.grid(row=0, column=1, padx=10)
        ttk.Button(nav, text=">", width=3, command=self.next_month).grid(row=0, column=2)

        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(pady=20)



    # ✅✅✅ === FUNGSI BARU: TOGGLE ===
    def toggle_cell(self, habit, date_str):
        """Klik = toggle ✅ / kosong"""

        data = self.data

        if date_str not in data:
            data[date_str] = []

        # Jika sudah ✅ → hapus
        if habit in data[date_str]:
            data[date_str].remove(habit)
        # Jika belum → tambahkan
        else:
            data[date_str].append(habit)

        save_calendar_log(data)
        self.data = load_calendar_log()
        self.render_table()



    # =====================
    #     RENDER TABLE
    # =====================
    def render_table(self):

        for w in self.table_frame.winfo_children():
            w.destroy()

        name = calendar.month_name[self.month]
        self.month_label.config(text=f"{name} {self.year}")

        num_days = calendar.monthrange(self.year, self.month)[1]

        # ===== HEADER =====
        ttk.Label(
            self.table_frame,
            text="Habit",
            font=("Helvetica", 10, "bold"),
            background="#4E8EF7",
            foreground="white",
            borderwidth=1,
            relief="ridge",
            width=20
        ).grid(row=0, column=0)

        for d in range(1, num_days + 1):
            lbl = tk.Label(
                self.table_frame,
                text=str(d),
                bg="#4E8EF7",
                fg="white",
                font=("Helvetica", 9, "bold"),
                width=3,
                relief="ridge",
                borderwidth=1
            )
            lbl.grid(row=0, column=d)


        # ===== ROW HABIT =====
        for r, habit in enumerate(self.habit_names):

            tk.Label(
                self.table_frame,
                text=habit,
                bg="#C9E9FF",
                fg="black",
                font=("Helvetica", 9, "bold"),
                width=20,
                relief="ridge",
                borderwidth=1
            ).grid(row=r+1, column=0)


            # ===== CELL =====
            for c in range(1, num_days + 1):
                date_str = f"{self.year}-{self.month:02d}-{c:02d}"

                cell_has = False
                if date_str in self.data and habit in self.data[date_str]:
                    cell_has = True

                text = "✅" if cell_has else ""
                bg_color = "#EAF6FF" if cell_has else "#FFFFFF"

                label = tk.Label(
                    self.table_frame,
                    text=text,
                    bg=bg_color,
                    fg="#0A4D68",
                    font=("Helvetica", 10),
                    width=3,
                    borderwidth=1,
                    relief="ridge"
                )
                label.grid(row=r+1, column=c)

                # ✅ BIND CLICK — tidak mengubah UI
                label.bind(
                    "<Button-1>",
                    lambda e, h=habit, d=date_str: self.toggle_cell(h, d)
                )



    # ===== NAV MONTH =====
    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.render_table()

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.render_table()
