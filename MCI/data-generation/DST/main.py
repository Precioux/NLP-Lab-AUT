import pandas as pd
from hazm import *
import re
import random


# LOADING GUIDE PART
# Load the Excel file into a DataFrame
excel_file_path = './source-v2.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
guide_dict = {}

for index, row in df.iterrows():
    slot = row['name']
    if type(slot) == str:
        guide_dict[slot] = []

        # Collect all examples from columns 'example-1' to 'example-12'
        for example_num in range(1, 1133):
            example_key = f'example-{example_num}'
            example_value = row[example_key]
            if not pd.isna(example_value):
                guide_dict[slot].append(example_value)

# print(guide_dict['city'])
#############################################################################################
# LOADING DATA
# Load the Excel file into a DataFrame
filename = 'dataset'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

data_dict = {}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in dfd.iterrows():
    # Check if the "Sample Question" column does not contain NaN values
    if not pd.isna(row['Sample Question']):
        sample_question = row['Sample Question']
        intent = row['intent']
        if intent not in data_dict:
            data_dict[intent]= {}
            data_dict[intent]['example']=[]
            data_dict[intent]['slots'] = []
        data_dict[intent]['example'].append(sample_question)

        # print(f'Q: {sample_question}')
        # print(f'intent : {intent}')

# print(data_dict)
# #################################################################################################
# LOADING ONTHOLOGY
# Load the Excel file into a DataFrame
filename = 'onthology'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

for index, row in dfd.iterrows():
    intent = row['intent']
    slot1 = row['slot1']
    m1 = row['1-mandatory']
    slot2 = row['slot2']
    m2 = row['2-mandatory']
    slot3 = row['slot3']
    m3 = row['3-mandatory']
    slot4 = row['slot4']
    m4 = row['4-mandatory']
    if intent in data_dict:
        if m1 == 1:
            data_dict[intent]['slots'].append(slot1)
        if m2 == 1:
            data_dict[intent]['slots'].append(slot2)
        if m3 == 1:
            data_dict[intent]['slots'].append(slot3)

# for key, value in data_dict.items():
#     print(key)
#     print(value['slots'])
#     # for v in value['slots']:
#     #     print(guide_dict[v])
# #################################################################################################
# LOADING questions
# Load the Excel file into a DataFrame
filename = 'questions'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

questions = {}
for index, row in dfd.iterrows():
    question = row['question']
    slot = row['slot']
    if slot not in questions:
        questions[slot]=[]
    questions[slot].append(question)

# print(questions)
# #################################################################################################
for intent, value in data_dict.items():
    print('Intent: ',intent)
    examples = value['example']
    slots = value['slots']
    for example in examples:
        print('Q: ', example)
        for slot in slots:
            print(f'searching for {slot}')
            exmps = guide_dict[slot]
            flag = 0
            for exmp in exmps:
                if exmp in example:
                    print(f'Slot {slot} is given!')
                    flag = 1
            if flag == 0:
                print(f'No data given for {slot}..lets ask')
                print(random.choice(questions[slot]))


