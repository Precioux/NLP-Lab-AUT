import os
import pandas as pd


def count_rows_by_writer(directory):
    writer_counts = {}

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)

            # Load the Excel file
            df = pd.read_excel(filepath)

            # Assuming the column containing writer's name is named 'writer'
            for index, row in df.iterrows():
                writer = row['writer']
                if writer not in writer_counts:
                    writer_counts[writer] = 1  # Initialize count for this writer
                else:
                    writer_counts[writer] += 1  # Increment count for this writer

            print(f'Processed file: {filename}')
            for key, value in writer_counts.items():
                print(f'{key}: {value}')

    return writer_counts


# Example usage:
directory = 'data/'
result = count_rows_by_writer(directory)
print(result)