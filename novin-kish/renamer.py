import os
import re
import shutil


def rename_and_move_json_files(source_directory, target_directory, start_num):
    # Ensure the target directory exists, create it if it doesn't
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Get a list of all files in the source directory
    files = os.listdir(source_directory)

    # Filter the files to only include JSON files and extract numbers from filenames
    json_files = [f for f in files if f.endswith('.json')]

    # Use regular expressions to extract the numeric part from each file name
    def extract_number(file_name):
        match = re.search(r'(\d+)', file_name)
        return int(match.group()) if match else -1

    # Sort files numerically based on the extracted number
    json_files.sort(key=extract_number)

    # Rename each JSON file starting from the given start number and move it to the target directory
    for idx, file_name in enumerate(json_files):
        # Construct the new file name starting from start_num
        new_file_name = f"data_{start_num + idx}.json"

        # Get the full paths for the old file and the new target file
        old_file_path = os.path.join(source_directory, file_name)
        new_file_path = os.path.join(target_directory, new_file_name)

        # Move the file to the target directory with the new name
        shutil.move(old_file_path, new_file_path)
        print(f"Renamed and moved {file_name} to {new_file_path}")


# Example usage:
source_directory = './test_json_files'  # Specify the source directory containing the JSON files
target_directory = './test-final'  # Specify the target directory
start_num = 210  # Specify the starting number for renaming
rename_and_move_json_files(source_directory, target_directory, start_num)