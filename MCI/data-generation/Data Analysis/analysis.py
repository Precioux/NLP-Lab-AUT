import pandas as pd
import os 


# Get the current directory (where the script is located)
folder_path = os.path.dirname(os.path.abspath(__file__))

# Get a list of all Excel files in the folder
excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
total_int = 0


# Iterate over each Excel file
for excel_file in excel_files:
    # Construct the full paths for input and output files
    xlsx_file = os.path.join(folder_path, excel_file)
    csv_file = os.path.splitext(excel_file)[0] + '.csv'

    # Convert XLSX to CSV
    data = pd.read_excel(xlsx_file)
    data.to_csv(csv_file, index=False)

    # Rest of your processing code
    try:
        csv_data = pd.read_csv(csv_file)

        # Initialize your counters and lists
        numberInt = 0
        writer_m_count = 0
        writer_s_count = 0
        writer_a_count = 0
        writer_ss_count = 0
        writer_g_count = 0
        writer_sh_count = 0
        writer_maz_count = 0
        writer_sob_count = 0
        writer_f_count = 0

        intents = []

        for index, row in csv_data.iterrows():
            # Process each row here
            intcheck = row['Intent - Eng']
            if intcheck not in intents:
                numberInt = numberInt + 1
                intents.append(intcheck)

            # Check if the 'writer' column value is 'م'
            if row['writer'] == 'م':
                writer_m_count += 1

            if row['writer'] == 'ث':
                writer_s_count += 1

            if row['writer'] == 'س':
                writer_ss_count += 1

            if row['writer'] == 'ا':
                writer_a_count += 1

            if row['writer'] == 'ق':
                writer_g_count += 1

            if row['writer'] == 'ش':
                writer_sh_count += 1

            if row['writer'] == 'ع':
                writer_maz_count += 1

            if row['writer'] == 'ص':
                writer_sob_count += 1

            if row['writer'] == 'ف':
                writer_f_count += 1

        # Rest of your processing for each row

        # Rest of your print statements
        print('File : ', excel_file)
        print('Number of Intents : ', numberInt)
        total_int = total_int + numberInt
        print(intents)
        print("Number of rows with writer 'ث':", writer_s_count)
        print("Number of rows with writer 'م':", writer_m_count)
        print("Number of rows with writer 'ا':", writer_a_count)
        print("Number of rows with writer 'ش':", writer_sh_count)
        print("Number of rows with writer 'ق':", writer_g_count)
        print("Number of rows with writer 'س':", writer_ss_count)
        print("Number of rows with writer 'ع':", writer_maz_count)
        print("Number of rows with writer 'ص':", writer_sob_count)
        print("Number of rows with writer 'ف':", writer_f_count)
        print("Total Data: ", writer_a_count + writer_m_count + writer_s_count + writer_ss_count + writer_g_count + writer_sh_count+ writer_maz_count+ writer_sob_count+writer_f_count)
        print('_______________________________________________________________________________________________')

    except pd.errors.EmptyDataError:
        print(f"The CSV file '{csv_file}' is empty or has no columns.")

print('Total intents :  ', total_int)