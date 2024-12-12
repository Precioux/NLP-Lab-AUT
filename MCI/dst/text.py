import pandas as pd

# Load the Excel file
file_path = 'convert_currency.xlsx'

# Read the data from the first sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')


# Define a function to handle subcolumn values in 'Slots'
def process_slots(slots_value):
    # Assuming subcolumns are separated by spaces, modify if needed
    if pd.isna(slots_value):
        return ''
    return ' '.join(slots_value.split())


# Apply the function to create a new 'slots' column
for index, row in df.iterrows():
    status = ''
    if row['speaker'] == 'done':
        status = 'completed'
    else:
        status = 'not-completed'
    if row['speaker'] == 'user':
        print(f'status: {status}')
        print(f'text: {row["text"]}')
        print(f'slots: {row["Slots"]}')
        print('----------------------------------------')

# # Select the required columns
# selected_columns = ['speaker', 'text', 'slots', 'intent']
# df_selected = df[selected_columns]
#
# # Save the result to a new Excel file
# output_file_path = 'processed_convert_currency.xlsx'
# df_selected.to_excel(output_file_path, index=False)
#
# # Display the processed dataframe
# print(df_selected.head())
