python
def print_non_empty_values(values, name_family_index):
    count = 1
    for row in values[1:]:  # Skip the header row
        if row[name_family_index] != '':
            print(f"{count}. {row[name_family_index]}")
            count += 1
