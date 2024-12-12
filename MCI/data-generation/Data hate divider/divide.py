import pandas as pd

# Load the Excel file into a DataFrame without header
excel_file_path = 'data-hate-3-f.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl', header=None)

# Initialize empty lists to store cells with "*" and without "*"
cells_political = []
cells_noraml= []
# Iterate through DataFrame rows
for index, row in df.iterrows():
    print(f'Index : {index}')
    political = row.iloc[:2]
    for cell in political:
        if isinstance(cell, str):
            print(f'{cell} added to political')
            cells_political.append(cell)
    normal = row.iloc[2:]
    for cell in normal:
        if isinstance(cell, str):
            print(f'{cell} added to normal')
            cells_noraml.append(cell)
    print('Political')
    print(cells_political)
    print('Normal')
    print(cells_noraml)



# Create DataFrames from the lists
df_cells_political = pd.DataFrame(cells_political, columns=['Political'])
df_cells_normal = pd.DataFrame(cells_noraml, columns=['Normal'])

# Export DataFrames to Excel files
with pd.ExcelWriter('data-hate-3-f-political.xlsx') as writer:
    df_cells_political.to_excel(writer, index=False)

with pd.ExcelWriter('data-hate-3-f-normal.xlsx') as writer:
    df_cells_normal.to_excel(writer, index=False)
