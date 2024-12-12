import pandas as pd

# Load the Excel file into a DataFrame without header
excel_file_path = 'data-hate-8-m.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl', header=None)

# Initialize empty lists to store cells with "*" and without "*"
cells_with_star = []
cells_without_star = []

# Iterate through DataFrame rows
for index, row in df.iterrows():
    print(f'Index : {index}')
    # Check if the fourth cell contains "*"
    cell_value = row.iloc[1]  # Access the second cell in the row
    if cell_value == '*':
        print('star found')
        cell_stared = row.iloc[0]
        cells = row.iloc[2:]
        if isinstance(cell_stared, str):
            print(f'{cell_stared} added to with stars')
            cells_with_star.append(cell_stared)
        for cell in cells:
            if isinstance(cell, str):
                print(f'{cell} added to without stars')
                cells_without_star.append(cell)

    else:
        cells= row.iloc[:3]
        for cell in cells:
            if isinstance(cell, str):
                print(f'{cell} added to without stars')
                cells_without_star.append(cell)

# Create DataFrames from the lists
df_cells_with_star = pd.DataFrame(cells_with_star, columns=['CellsWithStar'])
df_cells_without_star = pd.DataFrame(cells_without_star, columns=['CellsWithoutStar'])

# Export DataFrames to Excel files
with pd.ExcelWriter('data-hate-8-with-star.xlsx') as writer:
    df_cells_with_star.to_excel(writer, index=False)

with pd.ExcelWriter('data-hate-8-without-star.xlsx') as writer:
    df_cells_without_star.to_excel(writer, index=False)
