python
import requests

# Replace 'YOUR_API_ENDPOINT' with your actual SheetDB API endpoint
api_endpoint = 'YOUR_API_ENDPOINT'

# Make a GET request to get the data
response = requests.get(api_endpoint)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract unique names from the 'Name' column
    unique_names = set(entry['Name'] for entry in data if 'Name' in entry)
    
    if len(unique_names) > 0:
        print("Available names:")
        for name in unique_names:
            print(name)
        
        # Get user input for the name
        selected_name = input("Enter the name to retrieve the data from the 'Activity points' column: ")
        
        # Find the data for the selected name in the 'Activity points' column
        activity_points = None
        for entry in data:
            if 'Name' in entry and 'Activity points' in entry and entry['Name'] == selected_name:
                activity_points = entry['Activity points']
                break
        
        if activity_points is not None:
            print(f"Activity points for {selected_name}: {activity_points}")
            
            # Get user input for the new activity points value
            new_activity_points = input("Enter the new activity points value: ")
            
            # Update the 'Activity points' for the selected name
            for entry in data:
                if 'Name' in entry and 'Activity points' in entry and entry['Name'] == selected_name:
                    entry['Activity points'] = new_activity_points
            
            # Make a PATCH request to update the 'Activity points' for the selected name
            response = requests.patch(api_endpoint, json=data)
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"Activity points for {selected_name} updated successfully.")
            else:
                print("Failed to update activity points. Status code:", response.status_code)
            
        else:
            print(f"No data found for {selected_name}.")
    else:
        print("No data found in the Google Sheet.")
else:
    print("Failed to fetch data. Status code:", response.status_code)
