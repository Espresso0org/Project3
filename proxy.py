python
from colorama import Fore, Style

# Add the color formatting to the printed values
def print_non_empty_values(values, name_family_index):
    count = 1
    ranks_to_color = ["Deputy I", "Deputy II", "Deputy III", "Senior Deputy", "Corporal", "Sergeant", "Lieutenant"]
    
    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if row[name_family_index] in ranks_to_color:
            print(f"{count}. {Fore.MAGENTA}{row[name_family_index]}{Style.RESET_ALL}")
        else:
            print(f"{count}. {row[name_family_index]}")
        selected_rows.append(i)
        count += 1

# Main loop and other parts of the script remain the same
