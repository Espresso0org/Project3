python
import tkinter as tk
from tkinter import ttk

def manual_input_window(column_index, row_num, column_name):
    manual_input_window = tk.Toplevel(root)
    manual_input_window.title(f"Manual Input for {column_name}")

    prompt_label = tk.Label(manual_input_window, text=f"Enter points to add for {column_name}:")
    prompt_label.pack(pady=10)

    points_var = tk.IntVar()
    points_spinbox = tk.Spinbox(manual_input_window, from_=0, to=100, textvariable=points_var)
    points_spinbox.pack(pady=5)

    def confirm_input():
        points = points_var.get()
        if column_name == "Air Support points" or column_name == "Dispatch Points":
            points *= 3  # Multiply points by 3 for Air Support and Dispatch
        update_points(row_num, points, column_index, column_name)
        manual_input_window.destroy()

    confirm_button = ttk.Button(manual_input_window, text="Confirm", command=confirm_input)
    confirm_button.pack(pady=5)

# You can call this function with the appropriate arguments when needed.
