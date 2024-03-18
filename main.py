import tkinter as tk
import logging
from tkinter import ttk
from github import Github
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
import sys
from tkinter import messagebox
import gspread
import base64
from oauth2client.service_account import ServiceAccountCredentials
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import requests


from github import Github

# Authenticate with GitHub
token = "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"
file_path = "app.log"

g = Github(token)
repository_name = "kiomaku"
# Fetch repository
repo = g.get_user().get_repo(repository_name)

# Fetch file contents


# Write log messages








def fetch_credentials_from_github(username, repository_name, file_path):
    url = f"https://raw.githubusercontent.com/{username}/{repository_name}/main/{file_path}"
    response = requests.get(url)
    if response.status_code == 200:
        return tuple(response.text.strip().split(":"))  # Return credentials as a tuple
    else:
        print("Failed to fetch credentials from GitHub.")
        return None



def authenticate(username, password):
    # Fetch credentials from GitHub
    github_credentials = fetch_credentials_from_github("kiomaku", "kiomaku", "credentials.txt")
    
    if github_credentials and len(github_credentials) == 2:
        github_username, github_password = github_credentials  # Unpack credentials from the tuple
        # Compare with provided username and password
        if username == github_username and password == github_password:
            return True
    return False


def login():
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if authenticate(username, password):
            login_window.destroy()
            initialize_main_app()
            pass

# Commit changes
        else:
            mislog = (f"\nInvalid username or password {username}")
            messagebox.showerror("Error", "Invalid username or password")
            pass
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.iconbitmap('sheriff.ico')

    username_label = ttk.Label(login_window, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = ttk.Button(login_window, text="Login", command=verify_login)
    login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    login_window.mainloop()  

def initialize_main_app():
    import tkinter as tk
    from tkinter import ttk
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import tkinter.messagebox as messagebox
    def handle_command():
        command = console_entry.get().strip()
        if command:
            # Process command and update console output
            console_output.insert(tk.END, f">> {command}\n")
            console_output.insert(tk.END, "Command processing...\n")
            # Example command processing:
            if command == "help":
                console_output.insert(tk.END, "Available commands:\n")
                console_output.insert(tk.END, "- help: Display available commands\n")
                console_output.insert(tk.END, "- quit: Close the console\n")
            elif command == "quit":
                console_window.destroy()
            else:
                console_output.insert(tk.END, "Unknown command. Type 'help' for available commands.\n")
            console_output.see(tk.END)  # Scroll to the end of the console output
    def get_sheet_data():
        # Define the scope and credentials
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
        client = gspread.authorize(creds)

        # Access the Google Sheet by its URL
        sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1e0qbOssZGUDcwHN-GE99ZuknBTEpSCqjYWbAaYlIOzM/edit#gid=1097096341')

        # Select the first worksheet
        worksheet = sheet.get_worksheet(0)

        # Get all values and headers from the worksheet
        values = worksheet.get_all_values()
        headers = values[0]

        return worksheet, values, headers
    def get_sheet_data2():
            # Define the scope and credentials
            scope2 = ['https://www.googleapis.com/auth/spreadsheets']
            creds2 = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope2)
            client2 = gspread.authorize(creds2)

            # Access the Google Sheet by its URL
            sheet2 = client2.open_by_url('https://docs.google.com/spreadsheets/d/17zA2V2x-D3K-A01moq0IZ2JZ6qDYYYub/edit#gid=1261765202')

            # Select the first worksheet
            worksheet2 = sheet2.get_worksheet(0)

            # Get all values and headers from the worksheet
            values2 = worksheet2.get_all_values()
            headers2 = values2[0]

            return worksheet2, values2, headers2
    def apply_styles():
        style = ttk.Style()
        style.configure("Green.TButton", foreground="black", background="green")
        style.map("Green.TButton", foreground=[('pressed', 'black'), ('active', 'black')],
              background=[('pressed', '!disabled', 'green'), ('active', 'green')])
        style.configure("Blue.TButton", foreground="black", background="blue")
        style.map("Blue.TButton", foreground=[('pressed', 'black'), ('active', 'black')],
              background=[('pressed', '!disabled', 'blue'), ('active', 'blue')])
        # Configure Treeview
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#000000",
                        foreground="#ffffff",
                        fieldbackground="#000000",
                        rowheight=25)
        style.map("Treeview",
                background=[("selected", "#3498db")])
        # Configure Buttons
        style.configure("TButton",
                        foreground="#ffffff",
                        background="#3498db",
                        font=("Helvetica", 10, "bold"))
        style.map("TButton",
                background=[("active", "#2980b9")])

    def print_non_empty_values(values, name_family_index, sum_points_index):
        count = 1
        ranks_to_color = ["Deputy I", "Deputy II", "Deputy III", "Senior Deputy", "Corporal", "Sergeant", "Lieutenant"]
        
        for i, row in enumerate(values[1:], start=1):  # Skip the header row
            if row[name_family_index] != '':
                name = row[name_family_index]
                sum_points = row[sum_points_index]
                text = f"{count}. {name}"
                if name in ranks_to_color:
                    tree.insert("", "end", text=text, values=(sum_points,), tags=("rank",))
                else:
                    tree.insert("", "end", text=text, values=(sum_points,))
                selected_rows.append(i)
                count += 1

    def update_points(row_num, points, column_index, column_name):
        global worksheet, values, headers
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
        client = gspread.authorize(creds)

        # Access the Google Sheet by its URL
        sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1e0qbOssZGUDcwHN-GE99ZuknBTEpSCqjYWbAaYlIOzM/edit#gid=1097096341')

        # Select the first worksheet
        worksheet = sheet.get_worksheet(0)

        # Get all values and headers from the worksheet
        values = worksheet.get_all_values()
        headers = values[0]
        current_value = values[row_num][column_index].strip()  # Remove leading/trailing whitespace
        
        # Check if the current value is numeric or empty
        if current_value.isdigit():
            current_points = int(current_value)
            new_points = current_points + points
            worksheet.update_cell(row_num + 1, column_index + 1, str(new_points))
            print(f"{column_name} points updated successfully. Added {points} points to make {new_points}!")
            show_success_message(points, new_points)
        elif not current_value:  # If the cell is empty, treat it as zero
            worksheet.update_cell(row_num + 1, column_index + 1, str(points))
            print(f"{column_name} points updated successfully. Set to {points} points.")
            show_success_message(points, points)
        else:
            print(f"Error: Current value in {column_name} column is not numeric.")

        worksheet, values, headers = get_sheet_data()  
        tree.delete(*tree.get_children())  
        print_non_empty_values(values, name_family_index, sum_points_index)


    # Define hire_employee function
    def hire_employee():
        hire_window = tk.Toplevel(root)
        hire_window.title("Hire Employee")

        name_family_label = tk.Label(hire_window, text="Enter Name & Family:")
        name_family_label.pack(pady=10)

        name_family_entry = ttk.Entry(hire_window)
        name_family_entry.pack(pady=5)

        rank_label = tk.Label(hire_window, text="Select Rank Before:")
        rank_label.pack(pady=5)

        # Define rank options
        rank_options = ["Deputy I", "Deputy II", "Deputy III", "Senior Deputy", "Corporal", "Sergeant", "Lieutenant"]
        selected_rank = tk.StringVar(hire_window)
        selected_rank.set(rank_options[1])  # Default rank option

        # Dropdown menu for selecting rank
        rank_dropdown = ttk.OptionMenu(hire_window, selected_rank, *rank_options)
        rank_dropdown.pack(pady=5)

        def confirm_hire():
            new_name_family = name_family_entry.get().strip()
            rank_before = selected_rank.get()

            if new_name_family:
                empty_row_index = None
                for i, row in enumerate(values):
                    if row[name_family_index] == rank_before:
                        for j in range(i + 1, len(values)):
                            if not values[j][name_family_index]:
                                empty_row_index = j
                                break
                        break

                if empty_row_index is not None:
                    worksheet.update_cell(empty_row_index + 1, name_family_index + 1, new_name_family)
                    print(f"New employee {new_name_family} hired successfully.")
                    refresh_tab()
                    hire_window.destroy()
                else:
                    print("No empty row found after the specified rank.")
            else:
                messagebox.showerror("Error", "Please enter a valid name and family.")

        confirm_button = ttk.Button(hire_window, text="Confirm", command=confirm_hire)
        confirm_button.pack(pady=5)




    def show_success_message(points_added, total_points):
        success_window = tk.Toplevel(root)
        success_window.title("Success!")

        success_label = tk.Label(success_window, text=f"Successfully added {points_added} point(s). Total points now: {total_points}", fg="green")
        log_messages = (f"\nSuccessfully added {points_added} point(s). Total points now: {total_points}.")
        file_content = repo.get_contents(file_path)
        current_content = file_content.decoded_content.decode("utf-8")
        updated_content = current_content + log_messages
        repo.update_file(file_path, "Update log file", updated_content, file_content.sha)
        success_label.pack(padx=20, pady=10)

        def close_success_window():
            success_window.destroy()

        ok_button = ttk.Button(success_window, text="OK", command=close_success_window)
        ok_button.pack(pady=5)

    def on_select(event):
        selected_item = tree.selection()
        if selected_item:  # Check if any item is selected
            item = selected_item[0]
            row_text = tree.item(item, "text")  # Retrieve row text
            selected_name = row_text.split(". ", 1)[1]  # Extract selected name
            row_num_str = row_text.split(".", 1)[0]  # Extract row number string
            try:
                row_num = int(row_num_str)  # Convert the row number to an integer
                if 1 <= row_num <= len(selected_rows):
                    row_num = selected_rows[row_num - 1]
                    action_window(row_num, selected_name)  # Pass selected name to action_window
                else:
                    print("Row number is out of range.")
            except ValueError:
                print("Invalid row number.")
        else:
            print("No item selected.")

    def action_window(row_num, selected_name):  
        action_window = tk.Toplevel(root)
        action_window.title("Choose an Action")

        selected_name_label = tk.Label(action_window, text=f"Selected Name: {selected_name}")
        selected_name_label.pack(padx=20, pady=10)

        # Define options list
        options = [
            "10-10: Add 3 points to Rob status",
            "10-11: Add 1 point to Rob status",
            "Traffic Report: Add 2 points to Traffic report",
            "Activity Point: Manually specify points to add",
            "Document Report: Add 2 points to Document points",
            "H.R Points: Manually specify points to add",
            "Air Support Points: Manually specify points to add",
            "Dispatch Points: Manually specify points to add",
            "Back"
        ]

        # Create a Listbox for action options
        actions_listbox = tk.Listbox(action_window, selectmode=tk.SINGLE)
        actions_listbox.pack(padx=50, pady=5)

        # Populate the Listbox with options
        for option in options:
            actions_listbox.insert(tk.END, option)

        def handle_selection():
            selected_index = actions_listbox.curselection()
            if selected_index:
                selected_option = actions_listbox.get(selected_index[0])
                if selected_option == "Back":
                    action_window.destroy()
                else:
                    handle_action(selected_option, row_num)

        confirm_button = ttk.Button(action_window, text="Confirm", command=handle_selection)
        confirm_button.pack(pady=5)
    def handle_action(selected_option, row_num):
        global worksheet, values, headers
        if selected_option.startswith("10-10"):
            update_points(row_num, 3, rob_status_index, "Rob status points")
        elif selected_option.startswith("10-11"):
            update_points(row_num, 1, rob_status_index, "Rob status points")
        elif selected_option.startswith("Traffic Report"):
            update_points(row_num, 2, traffic_report_index, "Traffic report points")
        elif selected_option.startswith("Activity Point"):
            manual_input_window(activity_index, row_num, "Activity points")
        elif selected_option.startswith("Document Report"):
            update_points(row_num, 2, document_index, "Document points")
        elif selected_option.startswith("H.R Points"):
            manual_input_window(HR_index, row_num, "H.R Document points")
        elif selected_option.startswith("Air Support Points"):
            manual_input_window(air_index, row_num, "Air Support points")
        elif selected_option.startswith("Dispatch Points"):
            manual_input_window(dispatch_index, row_num, "Dispatch Points")
        elif selected_option.startswith("Back"):
            pass  # No action needed for "Back" option

    def manual_input_window(column_index, row_num, column_name):
        manual_input_window = tk.Toplevel(root)
        manual_input_window.title(f"Manual Input for {column_name}")

        prompt_label = tk.Label(manual_input_window, text=f"Enter points to add for {column_name}:")
        prompt_label.pack(pady=10)

        points_entry = ttk.Entry(manual_input_window)
        points_entry.pack(pady=5)

        def confirm_input():
            points_str = points_entry.get().strip()
            if points_str.isdigit():
                points = int(points_str)
                if column_name == "Air Support points" or column_name == "Dispatch Points":
                    points *= 3  # Multiply points by 3 for Air Support and Dispatch
                update_points(row_num, points, column_index, column_name)
                manual_input_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter a valid number.")

        confirm_button = ttk.Button(manual_input_window, text="Confirm", command=confirm_input)
        confirm_button.pack(pady=5)


    def search_name():
        search_query = search_entry.get().strip().lower()  # Convert search query to lowercase for case-insensitive search
        if search_query:
            found_items = []
            for item in tree.get_children():
                name = tree.item(item, "text").lower()  # Get the name of the current item in lowercase
                if search_query in name:
                    found_items.append(item)

            if found_items:
                tree.selection_set(found_items[0])  # Select the first found item
                tree.focus(found_items[0])  # Focus on the first found item
                tree.see(found_items[0])  # Ensure the selected item is visible
            else:
                messagebox.showinfo("Search Result", f"No results found for '{search_query}'.")
        else:
            messagebox.showwarning("Search", "Please enter a search query.")


    # Create a new frame for the search tab

    # Function to clear the search entry
    def clear_search_entry(event):
        search_entry.delete(0, "end")
    def refresh_tab():
        def close_app():
            root.destroy()
            initialize_main_app()  # Reopen the app
            
        close_app()
    def refresh_tab2():
        def close_loading_window():
            loading_window.destroy()

        loading_window = tk.Toplevel(root)
        loading_window.title("Loading...")
        loading_label = tk.Label(loading_window, text="Refreshing tab, please wait...")
        loading_label.pack(padx=20, pady=10)

        def refresh_data():
            global worksheet, values, headers
            # Clear the existing data displayed in the Treeview widget
            tree.delete(*tree.get_children())
            
            # Fetch the data again from the Google Sheets document
            worksheet, values, headers = get_sheet_data()
            
            # Populate the Treeview widget with the newly fetched data
            print_non_empty_values(values, name_family_index, sum_points_index)
            tree.tag_configure("colored", foreground="magenta")
            loading_window.after(1000, close_loading_window)  # Close loading window after 1 second

        loading_window.after(100, refresh_data)  # Call refresh_data after 100 milliseconds

    # Add the "Refresh" button
    def open_console():
        global console_window, console_entry, console_output
        console_window = tk.Toplevel(root)
        console_window.title("Custom Console")

        console_frame = ttk.Frame(console_window)
        console_frame.pack(fill="both", expand=True)

        console_output = ScrolledText(console_frame, wrap=tk.WORD, width=50, height=15)
        console_output.pack(fill="both", expand=True)

        console_entry = ttk.Entry(console_frame)
        console_entry.pack(side="left", fill="x", expand=True, padx=5)

        console_button = ttk.Button(console_frame, text="Execute", command=handle_command)
        console_button.pack(side="left", padx=5)
    # Main

    def bcsd_function():
        def get_sheet_data():
            # Define the scope and credentials
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
            client = gspread.authorize(creds)

            # Access the Google Sheet by its URL
            sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/17_PxptFCZiEPXhpPjFNXv9A1g7VDe99sH2nJlTsyECY/edit#gid=1097096341')

            # Select the first worksheet
            worksheet = sheet.get_worksheet(0)

            # Get all values and headers from the worksheet
            values = worksheet.get_all_values()
            headers = values[0]

            return values, headers

        def update_rank_lists():
            for rank in rank_lists:
                rank_lists[rank] = []

            for row in values[1:]:
                name = row[0]
                rank = row[3].strip()  # Assuming the rank is in the fourth column, and strip any leading/trailing spaces
                if rank:  # Check if the rank is not empty
                    if rank in rank_lists:  # Check if the rank exists in the dictionary
                        rank_lists[rank].append(name)
                    else:
                        print(f"Rank '{rank}' found in the spreadsheet but not in rank_lists.")

        def open_action_window(selected_name):
            action_window = tk.Toplevel(root2)
            action_window.title("Actions")

            # Your code for the action window here, using the selected_name
            # For example:
            label = tk.Label(action_window, text=f"Selected name: {selected_name}")
            label.pack()

        def on_select(event):
            selected_item = tree.selection()
            if selected_item:  # Check if any item is selected
                item = selected_item[0]
                row_text = tree.item(item, "text")  # Retrieve row text
                selected_name = row_text.split('. ', 1)[1] if '. ' in row_text else row_text
                open_action_window(selected_name)  # Pass selected name to action_window
            else:
                print("No item selected.")

        def fire_employee():
            selected_item = tree.selection()
            if selected_item:
                confirmed = messagebox.askyesno("Confirm", "Are you sure you want to fire this employee?")
                if confirmed:
                    # Extract the selected employee's name
                    selected_name = tree.item(selected_item[0], "text").split('. ', 1)[1]
                    
                    # Find the row number corresponding to the selected employee's name
                    row_num = None
                    for i, row in enumerate(values[1:], start=1):
                        if row[name_family_index] == selected_name:
                            row_num = i
                            break
                    
                    if row_num is not None:
                        # Clear all columns for the fired employee
                        for index, _ in enumerate(headers):
                            worksheet.update_cell(row_num + 1, index + 1, '')  # Clear all columns in the row

                        refresh_tab()  # Refresh the tab to reflect the changes
                    else:
                        messagebox.showerror("Error", "Failed to find the selected employee in the data.")
            else:
                messagebox.showinfo("Information", "Please select an employee to fire.")

        def refresh_function():
            root2.destroy()
            bcsd_function()    
        root2 = tk.Tk()
        root2.title("BCSD Roster")

        values, headers = get_sheet_data()

        columns_to_display = ['Name', 'Badge Number', 'Call Sign', 'Rank']

        filtered_headers = [header for header in headers if header in columns_to_display]
        filtered_values = [[row[headers.index(header)] for header in filtered_headers] for row in values]

        style = ttk.Style()
        style.configure("Green.TButton", foreground="black", background="green")
        style.map("Green.TButton", foreground=[('pressed', 'black'), ('active', 'black')],
                background=[('pressed', '!disabled', 'green'), ('active', 'green')])
        style.configure("Blue.TButton", foreground="black", background="blue")
        style.map("Blue.TButton", foreground=[('pressed', 'black'), ('active', 'black')],
                background=[('pressed', '!disabled', 'blue'), ('active', 'blue')])
        style.configure("Treeview",
                        background="#000000",
                        foreground="#ffffff",
                        fieldbackground="#000000",
                        rowheight=25)
        style.map("Treeview",
                background=[("selected", "#3498db")])

        frame = ttk.Frame(root2)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=filtered_headers, show='headings', style="Treeview")
        tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind("<Double-1>", on_select)
        for col in filtered_headers:
            tree.heading(col, text=col)

        # Insert data into the Treeview widget with numbering
        for i, row in enumerate(filtered_values[1:], start=1):
            tree.insert('', 'end', values=row, text=f"{i}. {row[0]}")

        button_frame = ttk.Frame(root2)
        button_frame.pack()

        refresh_button = ttk.Button(button_frame, text="Refresh", command=refresh_function, style="Blue.TButton")
        refresh_button.pack(side="left", padx=10, pady=10)

        rank_up_button = ttk.Button(button_frame, text="Fire", command=fire_employee)
        rank_up_button.pack(side="left", padx=10, pady=10)

        root2.mainloop()


    
    # Call the initialize_main_app() function to start the GUI application


    root = tk.Tk()
    # Set window properties
    root.title("Points Updater")
    root.iconbitmap('sheriff.ico')
    apply_styles()  # Apply styles before creating widgets

    worksheet, values, headers = get_sheet_data()

    name_family_index = headers.index("Name & Family")
    rob_status_index = headers.index("Rob status points")
    traffic_report_index = headers.index("Traffic report points")
    activity_index = headers.index("Activity points")
    document_index = headers.index("Document points")
    HR_index = headers.index("H.R Document points")
    air_index = headers.index("Air Support points")
    sum_points_index = headers.index("Sum points")  # New index for Sum points
    dispatch_index = headers.index("Dispatch Points")
    selected_rows = []

    tree = ttk.Treeview(root, selectmode="browse", columns=("Sum Points",))
    tree.heading("#0", text="Name & Family")
    tree.heading("#1", text="Sum Points", anchor="center")  # Align Sum Points values in the middle
    tree.column("#1", stretch=tk.YES)  # Allow stretching of Sum Points column
    tree.bind("<Double-1>", on_select)
    tree.pack(expand=True, fill="both")
    search_frame = ttk.Frame(root)
    search_frame.pack(side="top", fill="x")

    search_label = ttk.Label(search_frame, text="Search Name:")
    search_label.pack(side="left", padx=10, pady=10)

    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", padx=5, pady=10, fill="x", expand=True)

    search_button = ttk.Button(search_frame, text="Search", command=search_name)
    search_button.pack(side="left", padx=5, pady=10)
    # Bind the Entry to clear when clicked
    search_entry.bind("<Button-1>", clear_search_entry)
    print_non_empty_values(values, name_family_index, sum_points_index)
    tree.tag_configure("colored", foreground="magenta")
    tree.tag_configure("rank", foreground="green")


    def fire_employee():
        selected_item = tree.selection()
        if selected_item:
            confirmed = messagebox.askyesno("Confirm", "Are you sure you want to fire this employee?")
            if confirmed:
                # Extract the selected employee's name
                selected_name = tree.item(selected_item[0], "text").split('. ', 1)[1]
                
                # Find the row number corresponding to the selected employee's name
                row_num = None
                for i, row in enumerate(values[1:], start=1):
                    if row[name_family_index] == selected_name:
                        row_num = i
                        break
                
                if row_num is not None:
                    # Clear only the relevant columns for the fired employee
                    worksheet.update_cell(row_num + 1, name_family_index + 1, '')  # Clear the name column
                    for index, header in enumerate(headers):
                        if header != "Sum points":  # Skip "Sum points" column
                            worksheet.update_cell(row_num + 1, index + 1, '')  # Clear the individual points columns

                    refresh_tab()  # Refresh the tab to reflect the changes
                else:
                    messagebox.showerror("Error", "Failed to find the selected employee in the data.")
        else:
            messagebox.showinfo("Information", "Please select an employee to fire.")




    fire_frame = ttk.Frame(root)
    fire_frame.pack(side="top", fill="both", expand=True)


    hire_button = ttk.Button(root, text="Hire", command=hire_employee, style="Green.TButton")
    hire_button.pack(side="left", padx=10, pady=10)

    fire_button = ttk.Button(root, text="Fire", command=fire_employee)
    fire_button.pack(side="left", padx=10, pady=10)

    refresh_button = ttk.Button(root, text="Refresh", command=refresh_tab, style="Blue.TButton")
    refresh_button.pack(side="left", padx=10, pady=10)

    console_button = ttk.Button(root, text="Open Console", command=open_console)
    console_button.pack(side="left", padx=10, pady=10)

    bcsd_button = ttk.Button(root, text="BCSD", command=bcsd_function)
    bcsd_button.pack(side="left", padx=10, pady=10)
if __name__ == "__main__":
    login()
