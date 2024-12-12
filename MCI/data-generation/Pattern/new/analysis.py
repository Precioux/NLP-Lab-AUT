import pandas as pd
import os

def count_sentences_per_intent(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    print(df.columns.tolist())

    # Group by the 'intent' column and count the number of sentences for each intent
    intent_counts = df['intent'].value_counts()

    # Convert to a dictionary
    intent_counts_dict = intent_counts.to_dict()

    # Get the total number of sentences
    total_sentences = df.shape[0]

    return intent_counts_dict, total_sentences

def generate_report():
    # Get the current directory
    current_directory = os.getcwd()

    # Dictionary to store the report for each file
    report = {}

    # Iterate through all files in the current directory
    for filename in os.listdir(current_directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(current_directory, filename)
            intent_counts, total_sentences = count_sentences_per_intent(file_path)
            print(f'prossed file {file_path}')
            report[filename] = {
                'intent_counts': intent_counts,
                'total_sentences': total_sentences
            }

    return report

# Generate the report
report = generate_report()
total = 0
# Print the report
for filename, data in report.items():
    intent_counts = data['intent_counts']
    total_sentences = data['total_sentences']
    print(f'Report for {filename}:')
    print(f'  Total sentences: {total_sentences}')
    if filename != 'data_final.xlsx':
        total += total_sentences
    # for intent, count in intent_counts.items():
    #     print(f'  {intent}: {count} sentences')
    print()

# print(f'Total sentences: {total}')