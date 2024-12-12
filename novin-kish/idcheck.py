import os
import json
import pandas as pd

# Function to extract the intent_id from a JSON file
def extract_intent_id(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        intent_id = data.get('intent_id', None)  # Extract the intent_id (default to None if not found)
        return intent_id
    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None

# Function to process all JSON files in a directory and create an Excel summary
def create_summary_excel(directory_path, output_excel_path):
    file_intent_data = []

    # Iterate over all the files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):  # Process only JSON files
            json_file_path = os.path.join(directory_path, file_name)
            intent_id = extract_intent_id(json_file_path)
            file_intent_data.append({'file_name': file_name, 'intent_id': intent_id})

    # Create a DataFrame from the collected data
    df = pd.DataFrame(file_intent_data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=False)
    print(f"Summary file '{output_excel_path}' created successfully.")

# Example usage
directory_path = 'validation_json_files'  # Replace with the path to your directory containing JSON files
output_excel_path = 'summary-validation.xlsx'  # Replace with the path where you want to save the summary Excel file
create_summary_excel(directory_path, output_excel_path)
