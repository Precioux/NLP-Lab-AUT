import os
import json
import math


def is_nan(value):
    """Check if a value is NaN."""
    return isinstance(value, float) and math.isnan(value)


def get_json_files(directory):
    """Get a list of all JSON files in a directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]


def count_nan_records(file_path):
    """Count how many records have NaN in 'input_text'."""
    nan_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Check if 'input_text' is NaN
        if is_nan(data.get('input_text')):
            nan_count += 1
            print(f)

    return nan_count


def process_directory(directory):
    """Process all JSON files in a directory and count NaN records."""
    json_files = get_json_files(directory)
    total_nan_count = 0
    for json_file in json_files:
        total_nan_count += count_nan_records(json_file)
    return total_nan_count


def main(directories):
    total_nan_count = 0
    for directory in directories:
        total_nan_count += process_directory(directory)

    print(f"Total records with 'NaN' in 'input_text': {total_nan_count}")


if __name__ == "__main__":
    # List of directories containing JSON files
    directories = ['test', 'validation', 'train']  # Replace with actual directory paths
    main(directories)