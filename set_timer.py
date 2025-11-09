from tkinter import ttk, messagebox, simpledialog

def timer(self):
        try:
            new_work = simpledialog.askinteger("Set Work Time", "Masukkan durasi kerja (menit):", initialvalue=self.work_minutes, minvalue=1)
            if new_work is None:
                return

            new_break = simpledialog.askinteger("Set Break Time", "Masukkan durasi istirahat (menit):", initialvalue=self.break_minutes, minvalue=1)
            if new_break is None:
                return

            self.work_minutes = new_work
            self.break_minutes = new_break
            self.is_running = False
            self.is_work_session = True
            self.time_left = self.work_minutes * 60
            self.status_label.config(text="Status: Work Time")
            self.update_display()

            messagebox.showinfo("Waktu Diubah", f"Waktu kerja: {self.work_minutes} menit\nWaktu istirahat: {self.break_minutes} menit")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengubah waktu: {e}")