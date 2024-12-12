import pandas as pd

# Read the Excel file
filename = 'data_final'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')
print(dfd.columns.tolist())

dup = {}
s = []
data = []
# Iterate through the DataFrame rows and populate the dictionary
for index, row in dfd.iterrows():
    sentence = row['sentence']
    label = row['label']
    intent = row['intent']
    if sentence not in s:
        s.append(sentence)
        data.append([sentence, label, intent])
    else:
        if sentence in dup:
            dup[sentence]['count'] += 1
        else:
            dup[sentence] = {'label': label, 'intent': intent, 'count': 1}

# Create a new DataFrame with the collected data
columns = ['sentence', 'label', 'intent']
df_output = pd.DataFrame(data, columns=columns)

# Create a DataFrame for duplicates
dup_data = []
for sentence, info in dup.items():
    dup_data.append([sentence, info['label'], info['intent'], info['count']])
columns2 = ['sentence', 'label', 'intent', 'count']
df_output2 = pd.DataFrame(dup_data, columns=columns2)

# Export the new DataFrame to an Excel file
output_filename = filename + '-checked.xlsx'
output_filename2 = filename + '-duplicates.xlsx'

df_output.to_excel(output_filename, index=False)
df_output2.to_excel(output_filename2, index=False)

print(f'New Excel file saved as {output_filename}')
print(f'New Excel file saved as {output_filename2}')
