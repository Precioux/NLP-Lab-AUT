import pandas as pd

# Example to read another Excel file
filename = 'price'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

# # Print the column names to verify them
# print("Column names:", dfd.columns)

data = []
for index, row in dfd.iterrows():
    if not pd.isna(row['sentence']):
        sentence = row['sentence'].split()
        label = row['label'].split()
        nlabel = []
        flag = False
        for l in label:
            if l == 'b-coin_type':
                if flag == False:
                    nlabel.append(l)
                    flag = True
                else:
                    nlabel.append('i-coin_type')
            elif l == 'o':
                nlabel.append(l)
                flag = False
            else:
                nlabel.append(l)

        print(f'Sentence: {sentence}')
        print(f'label: {label}')
        print(f'nlabel: {nlabel}')

        sf = ' '.join(sentence)
        lf = ' '.join(nlabel)
        data.append([sf, lf])

# Create a new DataFrame with the collected data
columns = ['sentence','label']
df_output = pd.DataFrame(data, columns=columns)

# Export the new DataFrame to an Excel file
output_filename = filename + '-labeled-2.xlsx'
df_output.to_excel(output_filename, index=False)

print(f'New Excel file saved as {output_filename}')