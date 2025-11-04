from tkinter import ttk, messagebox, simpledialog
from utils import load_habits, save_habits
def delete(self):
    selected = self.habit_listbox.curselection()
    if not selected:
            messagebox.showwarning("Warning", "Please select a habit to delete!")
            return
    habit_name = list(self.habits.keys())[selected[0]]
    confirm = messagebox.askyesno("Delete Habit", f"Are you sure you want to delete '{habit_name}'?")
    if confirm:
            del self.habits[habit_name]
            save_habits(self.habits)
            self.refresh_list()