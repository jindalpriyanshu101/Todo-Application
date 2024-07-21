import customtkinter as ctk
import tkinter as tk
import csv
import os
import threading
import time
from win11toast import toast

class TodoApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        self.title("To-Do App")
        self.geometry("400x600")

        self.tasks = []
        self.reminders = {}
        self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        # Entry for new task
        self.task_entry = ctk.CTkEntry(self, width=300, placeholder_text="Enter a new task")
        self.task_entry.pack(pady=10)

        # Entry for reminder time
        self.reminder_entry = ctk.CTkEntry(self, width=300, placeholder_text="Enter reminder time in seconds")
        self.reminder_entry.pack(pady=10)

        # Add Task button
        self.add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self, width=50, height=15, font=("Helvetica", 14), justify=tk.CENTER, background="lightgrey")
        self.task_listbox.pack(pady=20)

        # Delete Task button
        self.delete_task_button = ctk.CTkButton(self, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=10)

        self.update_task_listbox()

    def add_task(self):
        task = self.task_entry.get()
        reminder_time = self.reminder_entry.get()

        if task:
            self.tasks.append(task)
            if reminder_time.isdigit():
                self.reminders[task] = int(reminder_time)
                self.set_reminder(task, int(reminder_time))
            self.update_task_listbox()
            self.task_entry.delete(0, ctk.END)
            self.reminder_entry.delete(0, ctk.END)
            self.save_tasks()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks.pop(selected_task_index[0])
            if task in self.reminders:
                del self.reminders[task]
            self.update_task_listbox()
            self.save_tasks()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def save_tasks(self):
        with open("Tasks.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                reminder_time = self.reminders.get(task, "")
                writer.writerow([task, reminder_time])

    def load_tasks(self):
        if os.path.exists("Tasks.csv"):
            with open("Tasks.csv", mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    task = row[0]
                    self.tasks.append(task)
                    if len(row) > 1 and row[1].isdigit():
                        reminder_time = int(row[1])
                        self.reminders[task] = reminder_time
                        self.set_reminder(task, reminder_time)

    def set_reminder(self, task, reminder_time):
        def reminder_loop():
            while task in self.tasks:
                time.sleep(reminder_time)
                if task in self.tasks:

                    # idhar function dalne ka kuchto jugaad bnana pdega 
                    notif_buttons = [
                        {'activationType': 'protocol', 'arguments': r'C:\Windows\Media\Alarm01.wav', 'content': 'Snooze'},

                        {'activationType': 'protocol', 'arguments': r'C:\Windows\Media\Alarm01.wav', 'content': 'Mark as Done'},

                        {'activationType': 'protocol', 'arguments': r'E:\Python\Python Projects\ScreenShot Parser\ques.py', 'content': 'Delete'}
                    ]
                    toast("Reminder", f"{task}", app_id="To-Do App", scenario='incomingCall', buttons = notif_buttons)

        reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
