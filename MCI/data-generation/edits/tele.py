import pandas as pd
from hazm import *
import re
import random
import openpyxl
from openpyxl.descriptors import slots

# LOADING GUIDE PART
# Load the Excel file into a DataFrame
excel_file_path = './guide.xlsx'
guide = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
guide_dict = {}
add_phrase = {'؟','ش','ها','!','ی','،','ه','م','ه؟','مون','','رو'}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in guide.iterrows():
    shorten_value = row['shorten value']
    if type(shorten_value) == str:
        sv_phrase = []
        for phrase in add_phrase:
            sv_phrase.append(row['shorten value'] + phrase)

        # Create a dictionary for the current shorten_value if it doesn't exist
        for sv in sv_phrase:
            if sv not in guide_dict:
                guide_dict[sv]={}

        # Populate the dictionary for the current shorten_value
        for sv in sv_phrase:
            guide_dict[sv]['real value'] = row['real value']
            guide_dict[sv]['name'] = row['name']
            guide_dict[sv]['example'] = []

        # Collect all examples from columns 'example-1' to 'example-108'
        for example_num in range(1, 109):
            example_key = f'example-{example_num}'
            example_value = row[example_key]
            if not pd.isna(example_value):
                for sv in sv_phrase:
                    guide_dict[sv]['example'].append(example_value)

# for key,value in guide_dict.items():
#     print(key)
#     print(value)

# Example to read another Excel file
filename = 'tele'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')


data = []
for index, row in dfd.iterrows():
    if not pd.isna(row['sentence']):
        sentence = row['sentence'].split()
        label = row['label'].split()
        if len(sentence) != len(label):
            print('error')
            print(sentence, label)
        else:
            print(sentence, label)


