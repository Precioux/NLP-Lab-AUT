import pandas as pd

guide_df = pd.read_excel('guide-bank.xlsx')

slots = {}
for index,row in guide_df.iterrows():
    slot = row['name']
    if slot not in slots:
        slots[slot] = 0

file_names = ['data-1-5']
for file_name in file_names:
    df = pd.read_excel('output-'+file_name+'.xlsx')
    for index, row in df.iterrows():
        label_str = str(row['slots'])
        label = label_str.split(' ')
        for slot in slots.keys():
            if (('b-'+slot) in label) or (('i-'+slot) in label):
                print(f'{slot} found in {label}')
                slots[slot] += 1

excel_data = []
for key, value in slots.items():
    excel_data.append([key, value])

columns = ('slot','static')
# Create a DataFrame from the excel_data list
df_excel = pd.DataFrame(excel_data, columns=columns)

# Save the DataFrame to an Excel file
excel_output_path = 'statistics.xlsx'
df_excel.to_excel(excel_output_path, index=False)
