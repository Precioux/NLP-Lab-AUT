import pandas as pd

# Read the Excel file
filename = 'data-checked'
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

# Print column names to check for correct column names
print("Column names in the DataFrame:", dfd.columns.tolist())

patterns = {}
intents = {}
samples = {}
pattern_id = 1
intent_id = 1
sample_id = 1


def intent_generator(intent_id):
    i = ''
    # Intent code
    if intent_id < 10:
        i = i + str('00' + str(intent_id))
    elif intent_id < 100:
        i = i + str('0' + str(intent_id))
    else:
        i = str(str(intent_id))
    return i


def pattern_generator(pid):
    p = ''
    # pattern code
    if pid < 10:
        p = p + str('00' + str(pid))
    elif pid < 100:
        p = p + str('0' + str(pid))
    else:
        p = str(pid)
    return p


def sample_generator(sample_id):
    s = ''
    # sample code
    if sample_id < 10:
        s = s + str('0' + str(sample_id))
    else:
        s = str(sample_id)
    return s


# Create a list to hold the rows for the new DataFrame
data = []
more = []

# Iterate through the DataFrame rows and populate the dictionary
for index, row in dfd.iterrows():
    # Check if the "sentence" column does not contain NaN values
    if not pd.isna(row['sentence']):
        sentence = row['sentence']
        intent = row['intent']
        # generating new intent id
        if intent not in intents:
            intents[intent] = intent_id
            intent_id = intent_id + 1
        label = row['label']
        s_tokens = sentence.split()
        l_tokens = label.split()
        print(s_tokens)
        print(len(s_tokens))
        if len(l_tokens) == len(s_tokens):
            # if len(s_tokens) < 15:
                new = []
                i = 0
                for l in l_tokens:
                    print(f'checking {l}')
                    if l == 'o':
                        print('marked as normal word')
                        new.append(s_tokens[i])
                    elif l.startswith('b'):
                        print('marked as slot word')
                        new.append(l_tokens[i])
                    i = i + 1
                n_sentence = ' '.join(new)
                # generating new sample id
                samples[n_sentence] = sample_id
                sample_id = sample_id + 1
                # generating new pattern id
                pid = 0
                sid = 0
                if n_sentence not in patterns:
                    patterns[n_sentence] = {}
                    patterns[n_sentence]['id'] = pattern_id
                    patterns[n_sentence]['tot'] = 1
                    pid = pattern_id
                    sid = patterns[n_sentence]['tot']
                    pattern_id = pattern_id + 1

                    i_id = intent_generator(intents[intent])
                    p_id = pattern_generator(pid)
                    s_id = sample_generator(sid)
                    IPS = i_id + p_id + s_id
                    print(sentence)
                    print(n_sentence)
                    print("*********************")

                    # Append row to the data list
                    data.append([s_id, p_id, i_id, i_id + p_id, IPS, sentence, label, intent])

                elif n_sentence in patterns and len(s_tokens) < 15:
                    pid = patterns[n_sentence]['id']
                    patterns[n_sentence]['tot'] = patterns[n_sentence]['tot'] + 1
                    sid = patterns[n_sentence]['tot']

                    i_id = intent_generator(intents[intent])
                    p_id = pattern_generator(pid)
                    s_id = sample_generator(sid)
                    IPS = i_id + p_id + s_id
                    print(sentence)
                    print(n_sentence)
                    print("*********************")

                    # Append row to the data list
                    data.append([s_id, p_id, i_id, i_id + p_id, IPS, sentence, label, intent])

                elif n_sentence in patterns and len(l_tokens) >= 15:
                    pid = patterns[n_sentence]['id']
                    more.append([pid, sentence, label, intent, len(s_tokens)])


            # else:
            #     more.append([sentence,label,intent, len(s_tokens)])

# Create a new DataFrame with the collected data
columns = ['sample id', 'pattern id', 'intent id', 'IP', 'IPS', 'sentence','label', 'intent']
df_output = pd.DataFrame(data, columns=columns)

# Export the new DataFrame to an Excel file
output_filename = filename + '-coded2.xlsx'
df_output.to_excel(output_filename, index=False)

columns2 = ['pattern ID','sentence','label', 'intent','length']
df_output2 = pd.DataFrame(more, columns=columns2)
output_filename2 = filename + '-more2.xlsx'
df_output2.to_excel(output_filename2, index=False)

print(f'New Excel file saved as {output_filename}')
