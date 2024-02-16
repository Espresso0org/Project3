python
from colorama import Fore, Style, init

# Initialize colorama
init()

selected_rows = []

def print_non_empty_values(values, name_family_index):
    count = 1
    ranks_to_color = ["Deputy I", "Deputy II", "Deputy III", "Senior Deputy", "Corporal", "Sergeant", "Lieutenant"]
    colored_ranks = []

    for i, row in enumerate(values[1:], start=1):  # Skip the header row
        if row[name_family_index] != '':
            if row[name_family_index] in ranks_to_color:
                colored_ranks.append(row[name_family_index])
            else:
                print(f"{count}. {row[name_family_index]}")
                selected_rows.append(i)
                count += 1

    # Display colored ranks separately with auto-assigned numbers
    for i, rank in enumerate(colored_ranks, start=1):
        print(f"{i}. {Fore.MAGENTA}{rank}{Style.RESET_ALL}")
