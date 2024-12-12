import pandas as pd
import json

# Read the Excel file
excel_file_path = './Onthology.xlsx'
df = pd.read_excel(excel_file_path)

# Create a dictionary to hold the data
domain_data = {}

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access values in each column for the current row
    index_value = row['index']
    domain = row['Domain']
    intent = row['intent']
    intent_per = row['مقصود']
    api = row['API']
    turn_type = row['Turn2']
    if row['check'] == 1:
        slot_check = 'yes'
    else :
        slot_check = 'no'
    slot1 = row['Slot1']
    slot2 = row['Slot2']
    slot3 = row['Slot3']
    slot4 = row['Slot4']

    if pd.notna(index_value):
        if domain not in domain_data:
            domain_data[domain] = []

        # Append intent data to the domain's list
        domain_data[domain].append({
            'intent': intent,
            'intent_per': intent_per,
            'API': api,
            'turn_type': turn_type,
            'slot_type': slot_check,
            'slot1': slot1,
            'slot2': slot2,
            'slot3': slot3,
            'slot4': slot4
        })

# Save the domain_data dictionary as a JSON file
json_output_path = 'output.json'
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(domain_data, json_file, ensure_ascii=False, indent=4)

print('JSON data has been written to', json_output_path)
