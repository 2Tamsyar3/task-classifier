import tkinter as tk
from tkinter import messagebox
import pandas as pd

class Task:
    def __init__(self, name, urgency, importance):
        self.name = name
        self.urgency = urgency
        self.importance = importance
    
    def quadrant(self):
        if self.urgency == "Important" and self.importance == "Urgent":
            return "Quadrant 1"
        elif self.urgency == "Important" and self.importance == "Not Urgent":
            return "Quadrant 2"
        elif self.urgency == "Not Important" and self.importance == "Urgent":
            return "Quadrant 3"
        else:
            return "Quadrant 4"

class App:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager")

        #welcomeLabel = tk.Label(master, text="Welcome to the Task Manager!")
        #welcomeLabel.pack()

        # Create task input fields
        tk.Label(master, text="Task Name").grid(row=0, column=0)
        self.task_name = tk.Entry(master)
        self.task_name.grid(row=0, column=1)

        tk.Label(master, text="Importance").grid(row=1, column=0)
        self.importance = tk.StringVar(value="Not Important")
        tk.OptionMenu(master, self.importance, "Important", "Not Important").grid(row=1, column=1)

        tk.Label(master, text="Urgency").grid(row=2, column=0)
        self.urgency = tk.StringVar(value="Not Urgent")
        tk.OptionMenu(master, self.urgency, "Urgent", "Not Urgent").grid(row=2, column=1)

        tk.Button(master, text="Add Task", command=self.add_task).grid(row=3, column=1)
        #tk.Button(master, text="Remove Task", command=self.remove_task).grid(row=3, column=2)

        # Create quadrants
        tk.Label(master, text="Important and Urgent: DO IT NOW!!!", bg="red", fg="white").grid(row=4, column=0)
        self.quadrant_1 = tk.Listbox(master, height=10, width=50)
        self.quadrant_1.grid(row=5, column=0)

        tk.Label(master, text="Important and Not Urgent: Please plan", bg="orange").grid(row=4, column=1)
        self.quadrant_2 = tk.Listbox(master, height=10, width=50)
        self.quadrant_2.grid(row=5, column=1)

        tk.Label(master, text="Not Important and Urgent: Delegate it", bg="yellow").grid(row=6, column=0)
        self.quadrant_3 = tk.Listbox(master, height=10, width=50)
        self.quadrant_3.grid(row=7, column=0)

        tk.Label(master, text="Not Important and Not Urgent: Ain't my business").grid(row=6, column=1)
        self.quadrant_4 = tk.Listbox(master, height=10, width=50)
        self.quadrant_4.grid(row=7, column=1)

        # Load existing tasks from file, if any
        try:
            self.tasks = pd.read_json("tasks.json")
            #print(self.tasks)
        except FileNotFoundError:
            self.tasks = pd.DataFrame(columns=["Name", "Importance", "Urgency"])
            #print(self.tasks)
            #self.tasks.to_json("tasks.json")

    def add_task(self):
        new_task = Task(self.task_name.get(), self.urgency.get(), self.importance.get())
        existing_task = self.tasks.loc[self.tasks['Name'] == new_task.name]

        if not existing_task.empty:
        # task already exists in the file, allow user to change urgency and importance
            existing_urgency = existing_task.iloc[0]['Urgency']
            existing_importance = existing_task.iloc[0]['Importance']
            message = f"A task with name '{new_task.name}' already exists: '{existing_importance}'and '{existing_urgency}'. Do you want to update it?"
            response = messagebox.askyesno("Task already exists", message)
            if response == tk.YES:
                self.tasks.loc[self.tasks['Name'] == new_task.name, ['Urgency', 'Importance']] = [new_task.urgency, new_task.importance]
                self.tasks.to_json("tasks.json")
                #self.write_task_to_json(task)
                self.check_quadrant(new_task.name, new_task.quadrant())
        else:
        # add new task to the file
            self.write_task_to_json(new_task)
            #self.check_quadrant(task)
            
    def check_quadrant(self, task_name, quadrant):
        # add task to the appropriate quadrant in the GUI       
        if quadrant == "Quadrant 1":
            self.quadrant_1.insert(tk.END, task_name)
        elif quadrant == "Quadrant 2":
            self.quadrant_2.insert(tk.END, task_name)
        elif quadrant == "Quadrant 3":
            self.quadrant_3.insert(tk.END, task_name)
        elif quadrant == "Quadrant 4":
            self.quadrant_4.insert(tk.END, task_name)

    def write_task_to_json(self, task):
         # Add a task to the tasks dataframe
        new_task_df = pd.DataFrame({
            "Name": [task.name],
            "Importance": [task.importance],
            "Urgency": [task.urgency]
        })

        self.tasks = pd.concat([self.tasks, new_task_df], ignore_index=True)
        self.tasks.to_json("tasks.json")

if __name__ == "__main__":
    root = tk.Tk()
    runTask = App(root)
    root.mainloop()


