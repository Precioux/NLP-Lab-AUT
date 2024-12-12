import pandas as pd

# Read the Excel file
fg = 'gm'
guide_file_path_data = './' + fg + '.xlsx'
dfg = pd.read_excel(guide_file_path_data, engine='openpyxl')

# Print the column names to verify them
# print("Column names:", dfg.columns)
guide = {'plus': [], 'minus': [], 'multiply': [], 'divide': [], 'radical': [], 'power': []}

# Example to read another Excel file
filename = 'math'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

for index, row in dfg.iterrows():
    if isinstance(row['plus'], str):
        guide['plus'].append(row['plus'])
    if isinstance(row['minus'], str) or isinstance(row['minus'], int):
        guide['minus'].append(str(row['minus']))
    if isinstance(row['multiply'], str):
        guide['multiply'].append(row['multiply'])
    if isinstance(row['divide'], str):
        guide['divide'].append(row['divide'])
    if isinstance(row['radical'], str):
        guide['radical'].append(row['radical'])
    if isinstance(row['power'], str):
        guide['power'].append(row['power'])

print(guide)
def check(labelstr):
    print('************************')
    label = labelstr.split()
    p = 0
    for l in label:
        print(f'checking {l}')
        if l == 'b-power' or l == 'b-divide' or l == 'b-plus' or l == 'b-minus' or l == 'b-radical' or l == 'b-multiply':
            print('found')
            p = p + 1

    print(label)
    print(p)
    print('************************')
    if p == 1:
        return True
    else:
        return False


data = []
more = []
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
            flag_plus = False
            flag_minus = False
            flag_multiply = False
            flag_divide = False
            flag_radical = False
            flag_power = False
            for s in sentence:
                if s in guide['plus']:
                    print(f'{s} is found as plus')
                    if not flag_plus:
                        l.append('b-' + 'plus')
                        flag_plus = True
                    else:
                        l.append('i-' + 'plus')
                elif s in guide['minus']:
                    print(f'{s} is found as minus')
                    if not flag_minus:
                        l.append('b-' + 'minus')
                        flag_minus = True
                    else:
                        l.append('i-' + 'minus')
                elif s in guide['divide']:
                    print(f'{s} is found as divide')
                    if not flag_divide:
                        l.append('b-' + 'divide')
                        flag_divide = True
                    else:
                        l.append('i-' + 'divide')
                elif s in guide['multiply']:
                    print(f'{s} is found as multiply')
                    if not flag_multiply:
                        l.append('b-' + 'multiply')
                        flag_multiply = True
                    else:
                        l.append('i-' + 'multiply')
                elif s in guide['power']:
                    print(f'{s} is found as power')
                    if not flag_power:
                        l.append('b-' + 'power')
                        flag_power = True
                    else:
                        l.append('i-' + 'power')
                elif s in guide['radical']:
                    print(f'{s} is found as radical')
                    if not flag_radical:
                        l.append('b-' + 'radical')
                        flag_radical = True
                    else:
                        l.append('i-' + 'radical')
                else:
                    l.append(label[i])
                    flag_plus = False
                    flag_minus = False
                    flag_divide = False
                    flag_multiply = False
                    flag_power = False
                    flag_radical = False
                i = i + 1
            print(l)
            sf = ' '.join(sentence)
            lf = ' '.join(l)
            f = check(lf)
            if f:
                data.append([sf, lf])
            else:
                more.append([sf, lf])

            # Create a new DataFrame with the collected data
        columns = ['sentence', 'label']
        df_output = pd.DataFrame(data, columns=columns)
        df_output2 = pd.DataFrame(more, columns=columns)

        # Export the new DataFrame to an Excel file
        output_filename = filename + '-labeled.xlsx'
        df_output.to_excel(output_filename, index=False)
        output_filename2 = filename + '-more.xlsx'
        df_output2.to_excel(output_filename2, index=False)

        print(f'New Excel file saved as {output_filename}')
