import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        
        self.conn = sqlite3.connect('tasks.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            description TEXT NOT NULL,
                            completed INTEGER NOT NULL DEFAULT 0
                          )''')
        self.conn.commit()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = tk.Button(self.button_frame, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.load_tasks()

    def add_task(self):
        task = self.entry.get()
        if task:
            self.c.execute("INSERT INTO tasks (description) VALUES (?)", (task,))
            self.conn.commit()
            self.entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def update_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            new_task = self.entry.get()
            if new_task:
                task_id = self.task_listbox.get(index).split(' ')[0]
                self.c.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_task, task_id))
                self.conn.commit()
                self.entry.delete(0, tk.END)
                self.load_tasks()
            else:
                messagebox.showwarning("Warning", "You must enter a task.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to update.")

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task_id = self.task_listbox.get(index).split(' ')[0]
            self.c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            self.conn.commit()
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to mark as complete.")

    def remove_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task_id = self.task_listbox.get(index).split(' ')[0]
            self.c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to remove.")

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.c.execute("SELECT id, description, completed FROM tasks")
        for row in self.c.fetchall():
            task = f"{row[0]} {row[1]}"
            if row[2] == 1:
                self.task_listbox.insert(tk.END, task)
                self.task_listbox.itemconfig(tk.END, {'bg':'lightgreen'})
            else:
                self.task_listbox.insert(tk.END, task)

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
