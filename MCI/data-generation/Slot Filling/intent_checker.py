import pandas as pd
from hazm import *
import re
import random


# Load the Excel file into a DataFrame
excel_file_path = './output-data9-8.5.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
data_dict = {}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in df.iterrows():
    shorten_value = row['intent']

    # Create a dictionary for the current shorten_value if it doesn't exist
    if shorten_value not in data_dict:
        data_dict[shorten_value] = 1

    else:
        data_dict[shorten_value] += 1

total = 0
for key, value in data_dict.items():
    print(f'{key} : {value}')
    total = total + value

print(f'Total : {total}')