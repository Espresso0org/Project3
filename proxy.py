python
# Add a list to store the actual row numbers
selected_rows = []

def print_non_empty_values(values, name_family_index):
    count = 1
    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if row[name_family_index] != '':
            print(f"{count}. {row[name_family_index]}")
            selected_rows.append(i)
            count += 1

# Main loop
while True:
    worksheet, values, headers = get_sheet_data()

    name_family_index = headers.index("Name & Family")
    rob_status_index = headers.index("Rob status points")
    traffic_report_index = headers.index("Traffic report points")
    activity_index = headers.index("Activity points")

    print_non_empty_values(values, name_family_index)
    print("Enter the row number to update points, or type 'back' to go back.")

    user_input = input("Your choice: ")

    if user_input.lower() == 'back':
        break
    elif user_input.isdigit():
        row_num = int(user_input)
        if 1 <= row_num <= len(selected_rows):
            row_num = selected_rows[row_num - 1]  # Get the actual row number
            print("1. 10-10 (Add 2 points to Rob status points)")
            print("2. 10-11 (Add 1 point to Rob status points)")
            print("3. Traffic report (Add 1 point to Traffic report points)")
            print("4. Activity point (Manually choose the number to add to Activity points)")

            action_input = input("Choose an action: ")
            if action_input == '1':
                update_points(row_num, 2, rob_status_index, "Rob status")
            elif action_input == '2':
                update_points(row_num, 1, rob_status_index, "Rob status")
            elif action_input == '3':
                update_points(row_num, 1, traffic_report_index, "Traffic report")
            elif action_input == '4':
                activity_points = int(input("Enter the number of points to add to Activity points: "))
                update_points(row_num, activity_points, activity_index, "Activity")
            else:
                print("Invalid action. Please try again.")
        else:
            print("Invalid row number. Please try again.")
    else:
        print("Invalid input. Please try again.")
