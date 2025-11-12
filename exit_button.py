import tkinter as tk
from tkinter import ttk, messagebox

def add_exit_button(parent):
    """
    Tambahkan tombol Exit ke frame atau window tertentu.
    parent: widget induk (biasanya frame utama atau ttk.Frame)
    """
    def confirm_exit():
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            parent.quit()  # Tutup seluruh aplikasi

    # buat frame untuk menampung tombol exit agar bisa sejajar
    exit_frame = ttk.Frame(parent)
    exit_button = ttk.Button(exit_frame, text="Exit", command=confirm_exit)
    exit_button.pack(pady=10)
    return exit_frame
