import pandas as pd
import json

# Read the Excel file
excel_file_path = './LoI.xlsx'
df = pd.read_excel(excel_file_path)

# Read the API Excel file
excel_file_path = './API.xlsx'
dfAPI = pd.read_excel(excel_file_path)
api_data = {}
for index, row in dfAPI.iterrows():
    id = row['id']
    if pd.notna(id):
        api_data[str(int(id))] = {
                'intent': row['intent'],
                'type': row['type']
            }
# print(api_data)
# Create a dictionary to hold the data
domain_data = {}
slot_dic = {}
# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access values in each column for the current row
    code = str(int(row['code']))
    index_value = row['index']
    domain = row['Domain']
    intent = row['intent']
    intent_per = row['مقصود']
    turn_type = row['Turn-1']
    if row['has slot'] == 1:
        slot_check = 'yes'
    else :
        slot_check = 'no'
    slots = {}

    # Populate the slot data dictionary
    m1 = row['1-mandatory']
    if m1 == 0:
        slots['slot1'] = {
            'title': row['Slot1'],
            'mandatory': row['1-mandatory'],
            'default': row['1-default']
        }
    elif m1 == 1:
        slots['slot1'] = {
            'title': row['Slot1'],
            'mandatory': row['1-mandatory'],
        }

    m2 = row['2-mandatory']
    if m2 == 0:
        slots['slot2'] = {
            'title': row['Slot2'],
            'mandatory': row['2-mandatory'],
            'default': row['2-default']
        }
    elif m2 == 1:
        slots['slot2'] = {
            'title': row['Slot2'],
            'mandatory': row['2-mandatory'],
        }

    m3 = row['3-mandatory']
    if m3 == 0:
        slots['slot3'] = {
            'title': row['Slot3'],
            'mandatory': row['3-mandatory'],
            'default': row['3-default']
        }
    elif m3==1:
        slots['slot3'] = {
            'title': row['Slot3'],
            'mandatory': row['3-mandatory'],
        }

    m4 = row['4-mandatory']
    if m4 == 0:
        slots['slot4'] = {
            'title': row['Slot4'],
            'mandatory': row['4-mandatory'],
            'default': row['4-default']
        }
    elif m4==1:
        slots['slot4'] = {
            'title': row['Slot4'],
            'mandatory': row['4-mandatory'],
        }

    if pd.notna(index_value):
        if domain not in domain_data:
            domain_data[domain] = []
        type = '-'
        print(f'Code : {code}')
        if code in api_data:
            type = api_data[code]["type"]
        # Append intent data to the domain's list
        if slot_check == 'yes':
            domain_data[domain].append({
                'code': code,
                'intent': intent,
                'intent_per': intent_per,
                'Source': type,
                'turn_type': turn_type,
                'has slot': slot_check,
                'slots' : slots
            })
        else:
            domain_data[domain].append({
                'code': code,
                'intent': intent,
                'intent_per': intent_per,
                'Source': type,
                'turn_type': turn_type,
                'has slot': slot_check
            })


# Save the domain_data dictionary as a JSON file
json_output_path = 'LoI.json'
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(domain_data, json_file, ensure_ascii=False, indent=4)

print('JSON data has been written to', json_output_path)
