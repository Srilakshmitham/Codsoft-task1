import tkinter as tk
from tkinter import messagebox

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do_List")

        self.tasks = []

        # Styling
        self.root.config(bg="#f0f0f0")
        self.font = ("Helvetica", 12)

        # Frame for buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(side=tk.TOP, padx=10, pady=(5, 0))

        # Entry for adding/updating tasks
        self.task_entry = tk.Entry(root, width=40, font=self.font, bg="#ffffff", bd=2, relief=tk.FLAT)
        self.task_entry.pack(side=tk.TOP, padx=10, pady=(0, 10), fill=tk.X)

        # Buttons
        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, font=self.font, bg="#4caf50", fg="#ffffff", bd=2, relief=tk.RAISED)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_button = tk.Button(button_frame, text="Status", command=self.toggle_status, font=self.font, bg="#ffc107", fg="#000000", bd=2, relief=tk.RAISED)
        self.status_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task, font=self.font, bg="#2196f3", fg="#ffffff", bd=2, relief=tk.RAISED)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task, font=self.font, bg="#ff5722", fg="#ffffff", bd=2, relief=tk.RAISED)
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Listbox with scrollbar
        self.task_listbox = tk.Listbox(root, width=50, height=15, font=self.font, bg="#ffffff", bd=2, relief=tk.FLAT, selectbackground="#2196f3", selectforeground="#ffffff")
        self.task_listbox.pack(side=tk.TOP, padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Bind double click event to update_task
        self.task_listbox.bind('<Double-Button-1>', lambda event: self.update_task())

        # Initialize the listbox with tasks (if any) from a saved file
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"description": task, "completed": False})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Empty Task", "Please enter a task.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove the selected task?")
            if confirm:
                task_index = selected_index[0]
                del self.tasks[task_index]
                self.update_task_listbox()
                self.save_tasks()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to remove.")

    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            updated_task = self.task_entry.get().strip()
            if updated_task:
                self.tasks[task_index]["description"] = updated_task
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showwarning("Empty Task", "Please enter a task.")
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to update.")

    def toggle_status(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.tasks[task_index]["completed"] = not self.tasks[task_index]["completed"]
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to toggle status.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else " "
            self.task_listbox.insert(tk.END, f"{status} {task['description']}")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = eval(file.read())  # Load tasks from the file
                self.update_task_listbox()  # Update the listbox with loaded tasks
        except FileNotFoundError:
            pass  # Ignore if the file does not exist or if there's an error reading it

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            file.write(repr(self.tasks))  # Save tasks to a file

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
