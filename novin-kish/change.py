import os
import json

# Path to the folder containing the JSON files
folder_path = "test"

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")

        # Open and load the JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
                continue

        # Check if the intent_id is 81
        if data.get("intent_id") == 81:
            print(f"Found intent_id 81 in {file_path}. Checking slots...")
            # Track if any changes are made
            made_changes = False

            # Iterate through the slots and change 'b-min_amount' to 'b-amount' and 'i-min_amount' to 'i-amount'
            for i, slot in enumerate(data["slots"]):
                if slot == "b-min_amount":
                    print(f"Changing 'b-min_amount' to 'b-amount' in file: {file_path}")
                    data["slots"][i] = "b-amount"
                    made_changes = True
                elif slot == "i-min_amount":
                    print(f"Changing 'i-min_amount' to 'i-amount' in file: {file_path}")
                    data["slots"][i] = "i-amount"
                    made_changes = True

            # Save the updated JSON back to the file if changes were made
            if made_changes:
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                print(f"Updated file: {file_path}")
            else:
                print(f"No changes needed in file: {file_path}")

print("Completed updating JSON files.")