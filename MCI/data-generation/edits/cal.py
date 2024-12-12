import pandas as pd

shamsi = {'شمسیه؟','شمسی', 'شمسیش', 'شمسیه', 'شمسیمو', 'شمسی،','شمسیشو','شمسیم','شمسی؟'}
miladi = {'میلادی،','میلادی', 'میلادیمو', 'میلادیه', 'میلادیش', 'میلادیه؟','میلادیشو','میلادی؟','میلادیم'}
ghamari = {'قمریه؟','قمریه','قمری،', 'قمریش', 'قمری', 'قمریمو', 'قمریشو','قمری؟','قمریم'}
# Example to read another Excel file
filename = 'cal3'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

# # Print the column names to verify them
# print("Column names:", dfd.columns)

data = []
for index, row in dfd.iterrows():
    if not pd.isna(row['sentence']):
        sentence = row['sentence'].split()
        label = row['label'].split()
        if len(sentence) == len(label):
            print(sentence)
            print(label)
            buf = []
            l = []
            flag_source = False
            flag_dest = False
            flag_shamsi = False
            flag_ghamari = False
            flag_miladi = False
            for s in sentence:
                if s in shamsi:
                    print('found in shamsi')
                    buf.append(s)
                    flag_shamsi = True
                elif s in miladi:
                    print('found in miladi')
                    buf.append(s)
                    flag_miladi = True
                elif s in ghamari:
                    print('found in ghamari')
                    buf.append(s)
                    flag_ghamari = True
            print(buf)
            print(flag_shamsi, flag_ghamari, flag_miladi)
            if (flag_shamsi and flag_ghamari and not flag_miladi) or (
                    flag_shamsi and flag_miladi and not flag_ghamari) or (
                    flag_ghamari and flag_miladi and not flag_shamsi):
                print('section 1')
                flag = False
                i = 0
                for s in sentence:
                    if (s in miladi or s in ghamari or s in shamsi) and flag == False:
                        l.append('b-source_calender')
                        flag = True
                    elif (s in miladi or s in ghamari or s in shamsi) and flag == True:
                        l.append('b-dest_calender')
                    else:
                        l.append(label[i])
                    i = i + 1
            elif (flag_shamsi and not flag_ghamari and not flag_miladi) or (flag_ghamari and not flag_shamsi and not flag_miladi) or (flag_miladi and not flag_ghamari and not flag_shamsi):
                print('section 2')
                i = 0
                for s in sentence:
                    if s in miladi or s in ghamari or s in shamsi:
                        l.append('b-dest_calender')
                    else:
                        l.append(label[i])
                    i = i + 1
            else:
                print('section 3')
                l = label
            print('final')
            print(l)
            sf = (' ').join(sentence)
            lf = (' ').join(l)
            data.append([sf,lf])
            print('*************************************')


            # Create a new DataFrame with the collected data
        columns = ['sentence', 'label']
        df_output = pd.DataFrame(data, columns=columns)

        # Export the new DataFrame to an Excel file
        output_filename = filename + '-labeled.xlsx'
        df_output.to_excel(output_filename, index=False)

        print(f'New Excel file saved as {output_filename}')