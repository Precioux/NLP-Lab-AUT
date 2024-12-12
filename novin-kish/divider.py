import pandas as pd

# Load the Excel file
file_path = 'final_data.xlsx'
excel_data = pd.ExcelFile(file_path)

# Load the data from the first sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Group by 'intent' and split into train and test sets
train_data = []
test_data = []
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

    else:
        print(f'intent {intent} is more than 10, {intents[intent]} added to train')
        train_data.append([row['text'], row['intent'], row['label']])
        intents[intent] += 1
        print('***************************************************')


print(check)

# Concatenate the lists into dataframes
col = ['text', 'intent', 'label']
# train_df = pd.concat(train_data)
# test_df = pd.concat(test_data)

# Save the train and test data to new Excel files
train_file_path = 'train_data.xlsx'
test_file_path = 'test_data.xlsx'

train_df = pd.DataFrame(train_data, columns=col)
test_df = pd.DataFrame(test_data, columns=col)

train_df.to_excel(train_file_path, index=False)
test_df.to_excel(test_file_path, index=False)

print(f'Train data saved to {train_file_path}')
print(f'Test data saved to {test_file_path}')