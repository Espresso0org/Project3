To add a virtual keyboard for entering names by mouse in your code, you can create a simple virtual keyboard interface as a separate component and integrate it with your existing search functionality. Here's an example implementation to help you get started:

```python
import tkinter as tk
from tkinter import messagebox

def search_name():
    search_query = search_entry.get().strip().lower()  # Convert search query to lowercase for case-insensitive search
    if search_query:
        found_items = []
        for item in tree.get_children():
            name = tree.item(item, "text").lower()  # Get the name of the current item in lowercase
            if search_query in name:
                found_items.append(item)

        if found_items:
            if len(found_items) == 1:
                tree.selection_set(found_items[0])  # Select the first found item
                tree.focus(found_items[0])  # Focus on the first found item
                tree.see(found_items[0])  # Ensure the selected item is visible
            else:
                current_index = found_items.index(tree.selection()[0]) if tree.selection() else -1
                next_index = (current_index + 1) % len(found_items)
                tree.selection_set(found_items[next_index])  # Select the next found item
                tree.focus(found_items[next_index])  # Focus on the next found item
                tree.see(found_items[next_index])  # Ensure the next selected item is visible
        else:
            messagebox.showinfo("Search Result", f"No results found for '{search_query}'.")
    else:
        messagebox.showwarning("Search", "Please enter a search query.")

# Create a virtual keyboard interface
def keypress(key):
    current_text = search_entry.get()
    search_entry.delete(0, tk.END)
    search_entry.insert(tk.END, current_text + key)

# GUI setup
root = tk.Tk()
search_entry = tk.Entry(root)
search_entry.pack()

# Sample virtual keyboard buttons
keyboard_frame = tk.Frame(root)
keyboard_frame.pack()

keys = "abcdefghijklmnopqrstuvwxyz"
for key in keys:
    btn = tk.Button(keyboard_frame, text=key, width=5, height=2,
                    command=lambda k=key: keypress(k))
    btn.grid(row=0, column=keys.index(key))

root.mainloop()
```

In the above code snippet, I added a virtual keyboard interface where each button press appends the corresponding character to the search query text entry field. You can customize the virtual keyboard further based on your requirements, such as adding more keys, styling, or functionalities.