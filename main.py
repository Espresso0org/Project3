python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)

# Access the Google Sheet by its URL
sheet = client.open_by_url('YOUR_GOOGLE_SHEET_URL')

# Select the first worksheet
worksheet = sheet.get_worksheet(0)

# Get all values and headers from the worksheet
values = worksheet.get_all_values()
headers = values[0]

# Find the index of the "Name & Family" column and "Rob status points" column
name_family_index = headers.index("Name & Family")
rob_status_index = headers.index("Rob status points")

def print_non_empty_values():
    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if row[name_family_index] != '':
            print(f"{i}. {row[name_family_index]}")

def update_rob_status_points(row_num, points):
    current_points = int(values[row_num][rob_status_index])
    new_points = current_points + points
    worksheet.update_cell(row_num + 1, rob_status_index + 1, str(new_points))
    print(f"Rob status points updated successfully to {new_points}!")

# Main loop
while True:
    print_non_empty_values()
    print("Enter the row number to update Rob status points, or type 'back' to go back.")

    user_input = input("Your choice: ")

    if user_input.lower() == 'back':
        break
    elif user_input.isdigit():
        row_num = int(user_input)
        if 1 <= row_num <= len(values) - 1:
            print("1. 10-10 (Add 2 points to Rob status points)")
            print("2. 10-11 (Add 1 point to Rob status points)")
            
            action_input = input("Choose an action: ")
            if action_input == '1':
                update_rob_status_points(row_num, 2)
            elif action_input == '2':
                update_rob_status_points(row_num, 1)
            else:
                print("Invalid action. Please try again.")
        else:
            print("Invalid row number. Please try again.")
    else:
        print("Invalid input. Please try again.")
