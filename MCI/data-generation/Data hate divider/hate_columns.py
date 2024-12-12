import pandas as pd

# Load your Excel file
df = pd.read_excel('data-hate-siasi-new.xlsx')

# Create a new DataFrame with just one column for the combined data
combined_column = pd.DataFrame(columns=['Combined'])

# Iterate through all columns and add non-empty cells to the first column
for col_num, column in enumerate(df.columns):
    combined_data = df[column].dropna()
    combined_column = combined_column.append(pd.DataFrame({'Combined': combined_data}), ignore_index=True)

    # Print the column number when adding to the output
    print(f"Added column {col_num}: {column}")

# Save the combined data to a new Excel file or overwrite the original file
combined_column.to_excel('data-hate-siasi-new-combined.xlsx', index=False)
