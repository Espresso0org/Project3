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
