from tkinter import messagebox, simpledialog
from utils import save_habits

def edit(self):
    selected = self.habit_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a habit to edit!")
        return

    old_name = list(self.habits.keys())[selected[0]]
    new_name = simpledialog.askstring("Edit Habit", f"Edit name for '{old_name}':", initialvalue=old_name)

    if new_name:
        new_name = new_name.strip()
        if new_name == "":
            messagebox.showwarning("Warning", "Habit name cannot be empty!")
            return

        # Cegah duplikasi nama habit
        if new_name != old_name and new_name in self.habits:
            messagebox.showwarning("Duplicate", "A habit with that name already exists!")
            return

        # Update nama habit
        self.habits[new_name] = self.habits.pop(old_name)
        save_habits(self.habits)
        self.refresh_list()
