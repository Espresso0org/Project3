python
def update_points(row_num, points, column_index, column_name):
    current_points = int(values[row_num][column_index]) if values[row_num][column_index] else 0
    new_points = current_points + points
    worksheet.update_cell(row_num + 1, column_index + 1, str(new_points))
    print(f"{column_name} points updated successfully to {new_points}!")
