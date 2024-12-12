import pandas as pd
from hazm import *
import re
import random
import openpyxl

# LOADING DATA
# Load the Excel file into a DataFrame
filename = 'output-telephone'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

# Print column names to check for correct column names
print("Column names in the DataFrame:", dfd.columns.tolist())

data_dict = {}
txtg = []
dup = {}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in dfd.iterrows():
    # Check if the "text" column does not contain NaN values
    if not pd.isna(row['text']):
        text = row['text']
        if text not in txtg:
            txtg.append(text)
            data_dict[text] = {
                'sample_id': row['sample_id'],
                'pattern_id - Per': row['pattern_id'],
                'slots': row['slots'],
                'intent': row['intent']  # Make sure this column exists in the DataFrame
            }
        else:
            if row['intent'] not in dup:
                dup[row['intent']] = []
            dup[row['intent']].append(text)

print('Data Checked. Duplicates: ')
for intent in dup:
    print(intent, dup[intent])
