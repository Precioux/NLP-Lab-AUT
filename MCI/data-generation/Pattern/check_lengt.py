import pandas as pd

# Read the Excel file
filename = 'data_phase1-checked-coded'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

for index, row in dfd.iterrows():
    sentence = row['sentence']
    tokens = sentence.split()
    if len(tokens) > 15 :
        print(sentence)