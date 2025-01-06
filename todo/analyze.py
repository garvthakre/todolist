import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

FILE_NAME = "tasks.csv"

# Function to load tasks from the CSV file
def load_tasks():
    try:
        df = pd.read_csv(FILE_NAME)
        # Check if 'Priority' column exists; if not, create it with a default value
        if 'Priority' not in df.columns:
            df['Priority'] = 'Medium'  # Assign a default value for missing 'Priority'
        df.rename(columns={"Name": "Task"}, inplace=True)  # Standardize column name to 'Task'
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=["Task", "Status", "Priority", "Expiry"])
        save_tasks(df)  # Create an empty file if it doesn't exist
        return df

# Function to save tasks to the CSV file
def save_tasks(df):
    df.to_csv(FILE_NAME, index=False)

# Function to refresh the task list in the UI
def refresh_task_list():
    df = load_tasks()
    task_listbox.delete(0, tk.END)  # Clear current listbox items
    for index, row in df.iterrows():
        task_text = f"{row['Task']} - {row['Status']} - {row['Priority']}"
        task_listbox.insert(tk.END, task_text)
    update_graph(df)  # Update the graph after refreshing task list
    update_progress(df)

# Function to mark a task as complete
def mark_complete():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_index = selected_task[0]
        df = load_tasks()
        task_name = df.loc[task_index, 'Task']
        df.loc[df['Task'] == task_name, 'Status'] = "Completed"
        save_tasks(df)
        refresh_task_list()
        messagebox.showinfo("Task Completed", f"Task '{task_name}' has been marked as completed.")
    else:
        messagebox.showwarning("No Selection", "Please select a task to mark as complete.")

# Function to add a new task
def add_task():
    task_name = task_entry.get()
    if task_name:
        priority = priority_combobox.get()
        expiry = expiry_entry.get()
        if expiry:
            df = load_tasks()
            new_task = pd.DataFrame({"Task": [task_name], "Status": ["Pending"], "Priority": [priority], "Expiry": [expiry]})
            df = pd.concat([df, new_task], ignore_index=True)
            save_tasks(df)
            refresh_task_list()
            task_entry.delete(0, tk.END)
            expiry_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an expiry date (YYYY-MM-DD).")
    else:
        messagebox.showwarning("Input Error", "Please enter a task name.")

# Function to delete a task
def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_index = selected_task[0]
        df = load_tasks()
        task_name = df.loc[task_index, 'Task']
        df = df.drop(task_index)
        save_tasks(df)
        refresh_task_list()
        messagebox.showinfo("Task Deleted", f"Task '{task_name}' has been deleted.")
    else:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

# Function to update the graph with task data
def update_graph(df):
    # Count the number of completed and pending tasks
    status_counts = df['Status'].value_counts()

    # Create a figure and axis for the bar chart
    fig, ax = plt.subplots(figsize=(5, 3))
    status_counts.plot(kind='bar', ax=ax, color=['#ff9999', '#66b3ff'])
    ax.set_title('Task Status')
    ax.set_ylabel('Count')
    ax.set_xlabel('Status')
    ax.set_xticklabels(status_counts.index, rotation=0)

    # Embed the figure in the Tkinter window
    for widget in frame_graph.winfo_children():
        widget.destroy()  # Remove any previous plot

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to update the progress bar
def update_progress(df):
    total_tasks = len(df)
    completed_tasks = len(df[df['Status'] == 'Completed'])
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    progress_bar["value"] = progress_percentage
    progress_label.config(text=f"Progress: {completed_tasks}/{total_tasks} tasks completed ({int(progress_percentage)}%)")

# Setting up the GUI
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x700")
root.config(bg="#f4f4f9")  # Set a nice background color

# Font style for the app
font_large = ("Helvetica", 14, "bold")
font_medium = ("Helvetica", 12)
font_small = ("Helvetica", 10)

# Header Label
header_label = tk.Label(root, text="Task Manager", font=("Helvetica", 20, "bold"), bg="#f4f4f9", fg="#333")
header_label.pack(pady=20)

# Entry to add tasks
task_entry = tk.Entry(root, width=40, font=font_medium, relief="solid", bd=2, highlightbackground="#bbb", highlightthickness=1)
task_entry.pack(pady=10)

# Combobox for task priority
priority_label = tk.Label(root, text="Priority:", font=font_small, bg="#f4f4f9")
priority_label.pack()
priority_combobox = ttk.Combobox(root, values=["Low", "Medium", "High"], state="readonly", font=font_medium)
priority_combobox.pack(pady=5)
priority_combobox.set("Medium")  # Default value

# Entry for task expiry date
expiry_label = tk.Label(root, text="Expiry Date (YYYY-MM-DD):", font=font_small, bg="#f4f4f9")
expiry_label.pack()
expiry_entry = tk.Entry(root, width=40, font=font_medium, relief="solid", bd=2, highlightbackground="#bbb", highlightthickness=1)
expiry_entry.pack(pady=10)

# Buttons for adding, marking as complete, and deleting tasks
button_frame = tk.Frame(root, bg="#f4f4f9")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", width=15, font=font_medium, bg="#4CAF50", fg="white", command=add_task, relief="flat")
add_button.grid(row=0, column=0, padx=10)

mark_button = tk.Button(button_frame, text="Mark Complete", width=15, font=font_medium, bg="#2196F3", fg="white", command=mark_complete, relief="flat")
mark_button.grid(row=0, column=1, padx=10)

delete_button = tk.Button(button_frame, text="Delete Task", width=15, font=font_medium, bg="#f44336", fg="white", command=delete_task, relief="flat")
delete_button.grid(row=0, column=2, padx=10)

# Progress bar for task completion
progress_label = tk.Label(root, text="Progress: 0/0 tasks completed", font=font_small, bg="#f4f4f9")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400, mode="determinate", maximum=100, value=0)
progress_bar.pack(pady=5)

# Listbox to display tasks
task_listbox = tk.Listbox(root, width=50, height=10, font=font_medium, bd=2, relief="solid", selectmode=tk.SINGLE)
task_listbox.pack(pady=10)

# Frame for the graph
frame_graph = tk.Frame(root, bg="#f4f4f9")
frame_graph.pack(pady=20)

# Refresh the task list and graph when the program starts
refresh_task_list()

root.mainloop()
