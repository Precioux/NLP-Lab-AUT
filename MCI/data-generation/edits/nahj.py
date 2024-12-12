import pandas as pd
# باب اول: خطبه‌ها و اوامر
# باب دوم: نامه‌ها و رسائل و وصایا
# باب سوم: کلمات قصار، حکمت‌آمیز و مواضع.

nahjcat = ['خطبه','پند','جملات', 'کلمات', 'قصار', 'حکمت','حکمتهای','خطبه‌های','اوامر','نامه','امر','نامه‌ها','نامه‌ی','نامه‌های']

# Example to read another Excel file
filename = 'nahj'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

# # Print the column names to verify them
# print("Column names:", dfd.columns)

data = []
for index, row in dfd.iterrows():
    if not pd.isna(row['sentence']):
        sentence = row['sentence'].split()
        label = row['label'].split()
        if len(sentence) != len(label):
            print('error')
            print(sentence, label)
        else:
            i = 0
            print(sentence)
            l = []
            flag_n = False
            for s in sentence:
                if s in nahjcat:
                    print(f'{s} is found as nahjcat')
                    if not flag_n:
                        l.append('b-' + 'nahjcat')
                        flag_n = True
                    else:
                        l.append('i-' + 'nahjcat')
                else:
                    l.append(label[i])
                    flag_n = False
                i = i + 1
            print(l)
            sf = ' '.join(sentence)
            lf = ' '.join(l)
            data.append([sf, lf])

            # Create a new DataFrame with the collected data
        columns = ['sentence', 'label']
        df_output = pd.DataFrame(data, columns=columns)

        # Export the new DataFrame to an Excel file
        output_filename = filename + '-labeled.xlsx'
        df_output.to_excel(output_filename, index=False)

        print(f'New Excel file saved as {output_filename}')
