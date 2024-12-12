import pandas as pd
import json
import os
import zipfile

# Load the Excel file
file_path = 'data-final.xlsx'
excel_data = pd.ExcelFile(file_path)

intents_file_path = 'intents.xlsx'

# Load the data from the first sheet
intents_df = pd.read_excel(intents_file_path)

# Create a dictionary to map intent names to their IDs
intent_mapping = dict(zip(intents_df['intent'], intents_df['intent_id']))

# Load the data from the first sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Group by 'intent' and split into train and test sets
train_data = []
test_data = []
validation_data = []
intents = {}
counter = 0
check = {}

for index, row in df.iterrows():
    print('***************************************************')
    print(f'row: {row}')
    intent = row['intent']
    if intent not in intents:
        counter = counter + 1
        check[intent] = counter
        print(f'new intent detected: {intent}')
        intents[intent] = 1
    if intents[intent] <= 10:
        print(f'intent: {intent} is less than 10, {intents[intent]} added to test')
        test_data.append([row['text'], row['intent'], row['label']])
        intents[intent] += 1
        print('***************************************************')
    elif 15 >= intents[intent] >= 11:
        print(f'intent: {intent} is more than 11, {intents[intent]} added to validation')
        validation_data.append([row['text'], row['intent'], row['label']])
        intents[intent] += 1
        print('***************************************************')
    else:
        print(f'intent {intent} is more than 10, {intents[intent]} added to train')
        train_data.append([row['text'], row['intent'], row['label']])
        intents[intent] += 1
        print('***************************************************')

print(check)

# Define columns
col = ['text', 'intent', 'label']

# Convert lists to DataFrames
train_df = pd.DataFrame(train_data, columns=col)
test_df = pd.DataFrame(test_data, columns=col)
validation_df = pd.DataFrame(validation_data, columns=col)

# Directory to save individual JSON files
train_json_dir = 'train_json_files'
test_json_dir = 'test_json_files'
validation_json_dir = 'validation_json_files'

print(f'Train data : {len(train_data)}')
print(f'Test data : {len(test_data)}')
print(f'Validation data: {len(validation_data)}')

for dir_path in [train_json_dir, test_json_dir, validation_json_dir]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Function to save each row as a JSON file
def save_json_files(df, json_dir):
    for idx, row in df.iterrows():
        text = row['text']
        intent_id = intent_mapping.get(row['intent'], -1)
        # Handle NaN values in 'label' column
        if pd.isna(row['label']):
            slots = []
        else:
            slots = row['label'].split()
        json_data = {
            'input_text': text,
            'intent_id': intent_id,
            'slots': slots
        }
        json_file_path = os.path.join(json_dir, f'data_{idx}.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# Save DataFrames to JSON files
save_json_files(train_df, train_json_dir)
save_json_files(test_df, test_json_dir)
save_json_files(validation_df, validation_json_dir)

# Function to create a ZIP file containing all JSON files
def create_zip_file(json_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(json_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

# Create ZIP files for train and test data
train_zip_file_path = 'train-part2.zip'
test_zip_file_path = 'test-part2.zip'
validation_zip_file_path = 'validation-part2.zip'

create_zip_file(train_json_dir, train_zip_file_path)
create_zip_file(test_json_dir, test_zip_file_path)
create_zip_file(validation_json_dir, validation_zip_file_path)

print(f'Train data JSON files saved and zipped at: {train_zip_file_path}')
print(f'Test data JSON files saved and zipped at: {test_zip_file_path}')
print(f'Validation data JSON files saved and zipped at: {validation_zip_file_path}')