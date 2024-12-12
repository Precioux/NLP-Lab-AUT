import pandas as pd
import os

# Get the current directory (where the script is located)
folder_path = os.path.dirname(os.path.abspath(__file__))

# Create a list to store the data for export
export_data = []

# Get a list of all Excel files in the folder
excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
total_int = 0

# Iterate over each Excel file
for excel_file in excel_files:
    # Construct the full paths for input and output files
    xlsx_file = os.path.join(folder_path, excel_file)
    csv_file = os.path.splitext(excel_file)[0] + '.csv'
    print(f'Processing file : {excel_file}')

    # Convert XLSX to CSV
    data = pd.read_excel(xlsx_file)
    data.to_csv(csv_file, index=False)

    # Rest of your processing code
    try:
        csv_data = pd.read_csv(csv_file)

        # Initialize your counters and dictionaries
        numberInt = 0
        intents = {}
        intents_d = {}
        for index, row in csv_data.iterrows():
            # Process each row here
            intcheck = row['Intent - Eng']
            if intcheck not in intents_d:
                intents_d[intcheck]=row['No']
            # Check if 'Sample Question' is not NaN before processing
            if pd.notna(row['Sample Question']):
                if intcheck not in intents:
                    numberInt = numberInt + 1
                    intents[intcheck] = 1
                else:
                    intents[intcheck] = intents[intcheck] + 1

        # Append data for export
        for intent, value in intents.items():
            export_data.append({'Excel File Name': excel_file, 'Intent Name': intent, 'Intent ID': intents_d.get(intent),'Value of Intent': value})

        # Rest of your processing for each row

        # Rest of your print statements
        print('File : ', excel_file)
        print('Number of Intents : ', numberInt)
        total_int = total_int + numberInt
        print(intents)
        print('_______________________________________________________________________________________________')

    except pd.errors.EmptyDataError:
        print(f"The CSV file '{csv_file}' is empty or has no columns.")

# Create a DataFrame from the export data
export_df = pd.DataFrame(export_data)

# Save the DataFrame to an Excel file
export_excel_file = os.path.join(folder_path, 'intent_export.xlsx')
export_df.to_excel(export_excel_file, index=False)

print('Total intents :  ', total_int)
