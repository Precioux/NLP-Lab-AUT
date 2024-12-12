
import os
import json
from collections import defaultdict
import pandas as pd

def get_json_files(directory):
    """Get a list of all JSON files in a directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]

def process_file(file_path, intent_counts, slot_counts):
    """Read a JSON file and update intent and slot statistics."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Count intent_id
        intent_id = data.get('intent_id')
        intent_counts[intent_id] += 1
        
        # Count slots
        slots = data.get('slots', [])
        for slot in slots:
            slot_counts[slot] += 1

def process_directory(directory, intent_counts, slot_counts):
    """Process all JSON files in a directory."""
    json_files = get_json_files(directory)
    for json_file in json_files:
        process_file(json_file, intent_counts, slot_counts)

def main(directories, output_file):
    # Initialize counters
    intent_counts = defaultdict(int)
    slot_counts = defaultdict(int)

    # Process each directory
    for directory in directories:
        process_directory(directory, intent_counts, slot_counts)

    # Create DataFrame for intent counts
    intent_df = pd.DataFrame(list(intent_counts.items()), columns=['Intent ID', 'Occurrences'])

    # Create DataFrame for slot label counts
    slot_df = pd.DataFrame(list(slot_counts.items()), columns=['Slot Label', 'Occurrences'])

    # Write to Excel
    with pd.ExcelWriter(output_file) as writer:
        intent_df.to_excel(writer, sheet_name='Intent Statistics', index=False)
        slot_df.to_excel(writer, sheet_name='Slot Statistics', index=False)

if __name__ == "__main__":
    # List of directories containing JSON files
    directories = ['validation','test','train']  # Replace with actual directory paths
    output_file = 'statistics_output.xlsx'  # Replace with desired output file path
    main(directories, output_file)
