import os
import json
import pandas as pd
import math


def is_nan(value):
    """Check if a value is NaN."""
    return isinstance(value, float) and math.isnan(value)


def get_json_files(directory):
    """Get a list of all JSON files in a directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]


def load_corrections(excel_file):
    """Load the correct 'input_text' values and other fields from an Excel file."""
    corrections = pd.read_excel(excel_file)
    return corrections.set_index('intent_id').to_dict()['correct_input_text']


def clean_nan_records(data, corrections):
    """Clean records with NaN input_text and replace them with correct data."""
    if is_nan(data.get('input_text')):
        intent_id = data.get('intent_id')

        # Replace NaN input_text with correct input_text from the corrections data
        if intent_id in corrections:
            print(f"Replacing NaN for intent_id {intent_id} with '{corrections[intent_id]}'")
            data['input_text'] = corrections[intent_id]
        else:
            print(f"No correction found for intent_id {intent_id}, setting input_text to an empty string.")
            data['input_text'] = ""  # Set to empty string if no correction is available

    return data


def process_file(file_path, corrections):
    """Read a JSON file, clean records, and save the cleaned version."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Clean the data if NaN is found in input_text
        cleaned_data = clean_nan_records(data, corrections)

    # Save the cleaned data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)


def process_directory(directory, corrections):
    """Process all JSON files in a directory and clean them."""
    json_files = get_json_files(directory)
    for json_file in json_files:
        process_file(json_file, corrections)


def main(directories, excel_file):
    # Load the correct values from the Excel file
    corrections = load_corrections(excel_file)

    # Process each directory
    for directory in directories:
        process_directory(directory, corrections)


if __name__ == "__main__":
    # List of directories containing JSON files
    directories = ['dir1', 'dir2', 'dir3']  # Replace with actual directory paths
    excel_file = '/path/to/corrections.xlsx'  # Replace with the actual path to the Excel file
    main(directories, excel_file)