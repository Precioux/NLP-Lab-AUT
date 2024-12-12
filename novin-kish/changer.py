import os
import json
import pandas as pd

def get_json_files(directory):
    """Get a list of all JSON files in a directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]

def load_corrections(excel_file):
    """Load the 'wrong' and 'correct' mappings from an Excel file."""
    corrections = pd.read_excel(excel_file)
    return dict(zip(corrections['wrong'], corrections['correct']))

def replace_slots(slots, corrections):
    """Replace wrong values in the slots array, preserving the 'b-' and 'i-' prefixes."""
    corrected_slots = []
    changes = []

    for slot in slots:
        if slot.startswith("b-") or slot.startswith("i-"):
            # Extract the prefix (b- or i-)
            prefix = slot[:2]
            # Remove the prefix to check against corrections
            base_slot = slot[2:]

            # If the base slot is in corrections, replace it and keep the prefix
            if base_slot in corrections:
                corrected_slot = prefix + corrections[base_slot]
                changes.append((slot, corrected_slot))  # Log the change
                corrected_slots.append(corrected_slot)
            else:
                corrected_slots.append(slot)
        else:
            corrected_slots.append(slot)

    return corrected_slots, changes

def process_file(file_path, corrections):
    """Read a JSON file, replace wrong slot values, and log changes."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Only modify the 'slots' field if it exists
        if 'slots' in data:
            corrected_slots, changes = replace_slots(data['slots'], corrections)
            data['slots'] = corrected_slots

            # Print the changes made
            for old, new in changes:
                print(f"Replaced '{old}' with '{new}' in {file_path}")

    # Save the corrected data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_directory(directory, corrections):
    """Process all JSON files in a directory."""
    json_files = get_json_files(directory)
    for json_file in json_files:
        process_file(json_file, corrections)

def main(directories, excel_file):
    # Load the corrections from the Excel file
    corrections = load_corrections(excel_file)

    # Process each directory
    for directory in directories:
        process_directory(directory, corrections)

if __name__ == "__main__":
    # List of directories containing JSON files
    directories = ['train', 'test', 'validation']  # Replace with actual directory paths
    excel_file = 'change.xlsx'  # Replace with the actual path to the Excel file
    main(directories, excel_file)