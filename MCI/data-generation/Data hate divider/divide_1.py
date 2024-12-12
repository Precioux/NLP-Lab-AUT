import pandas as pd

# Load the Excel file into a DataFrame without header
excel_file_path = 'TODO.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl', header=None)

# Initialize empty lists to store cells with "*" and without "*"
cells_with_one = []
cells_without_one = []

# Iterate through DataFrame rows
for index, row in df.iterrows():
    print(f'Index : {index}')
    # Check if the fourth cell contains "*"
    cell_value = row.iloc[1]  # Access the second cell in the row
    print(f'{cell_value} , {type(cell_value)}')
    if cell_value == 1:
        print('one found')
        cell_stared = row.iloc[0]
        print(f'{cell_stared} added to with stars')
        cells_with_one.append(cell_stared)
    else:
        cell = row.iloc[0]
        cells_without_one.append(cell)

# Create DataFrames from the lists
df_cells_with_star = pd.DataFrame(cells_with_one, columns=['cellswith1'])
df_cells_without_star = pd.DataFrame(cells_without_one, columns=['cellswithout1'])

# Export DataFrames to Excel files
with pd.ExcelWriter('todo-with1.xlsx') as writer:
    df_cells_with_star.to_excel(writer, index=False)

with pd.ExcelWriter('todo-without1.xlsx') as writer:
    df_cells_without_star.to_excel(writer, index=False)
