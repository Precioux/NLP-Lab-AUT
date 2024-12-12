import pandas as pd
from hazm import *
import re
import random
import openpyxl
from openpyxl.descriptors import slots

# LOADING GUIDE PART
# Load the Excel file into a DataFrame
excel_file_path = './guide.xlsx'
guide = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
guide_dict = {}
add_phrase = {'؟','ش','ها','!','ی','،','ه','م','ه؟','مون','','رو'}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in guide.iterrows():
    shorten_value = row['shorten value']
    if type(shorten_value) == str:
        sv_phrase = []
        for phrase in add_phrase:
            sv_phrase.append(row['shorten value'] + phrase)

        # Create a dictionary for the current shorten_value if it doesn't exist
        for sv in sv_phrase:
            if sv not in guide_dict:
                guide_dict[sv]={}

        # Populate the dictionary for the current shorten_value
        for sv in sv_phrase:
            guide_dict[sv]['real value'] = row['real value']
            guide_dict[sv]['name'] = row['name']
            guide_dict[sv]['example'] = []

        # Collect all examples from columns 'example-1' to 'example-108'
        for example_num in range(1, 109):
            example_key = f'example-{example_num}'
            example_value = row[example_key]
            if not pd.isna(example_value):
                for sv in sv_phrase:
                    guide_dict[sv]['example'].append(example_value)

# for key,value in guide_dict.items():
#     print(key)
#     print(value)
###########################################################################
# LOADING DATA
# Load the Excel file into a DataFrame
filename = ('telephone')
excel_file_path_data = './' + filename + '.xlsx'
dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

data_dict = {}
sqs = []

# Iterate through the DataFrame rows and populate the dictionary
for index, row in dfd.iterrows():
    # Check if the "Sample Question" column does not contain NaN values
    if not pd.isna(row['Sample Question']):
        sample_question = row['Sample Question']
        sqs.append(sample_question)
        data_dict[sample_question] = {
            'Intent - Eng': row['Intent - Eng']
        }
# for key,value in data_dict.items():
#     print(key)
#     print(value)
###########################################################################
# Preprocess the sample questions
normalizer = Normalizer()
stemmer = Stemmer()
for key, value in data_dict.items():
    # Tokenize
    tokens = key.split()

    # Store the result in the dictionary
    value['tokenized'] = tokens
    value['slots'] = []
    value['slot'] = 0

    for w in tokens:
        # print(f'w={w}')
        if w in guide_dict:
            # print(f'slot founded : {guide_dict[w]}')
            value['slot'] = 1
            value['slots'].append(w)

def preprocess(sq):
    # Tokenize
    tokens = sq.split()
    return tokens

# for key,value in data_dict.items():
#     print(key)
#     print(value)
###########################################################################
def min_example_number(slots):
    num = []
    for slot in slots:
        if slot in guide_dict:
            # print(slot)
            # print(len(guide_dict[slot]['example']))
            num.append(len(guide_dict[slot]['example']))
    result = min(num)
    print(f'Min : {result}')
    return result

def max_example_number(slots):
    num = []
    for slot in slots:
        if slot in guide_dict:
            # print(slot)
            # print(len(guide_dict[slot]['example']))
            num.append(len(guide_dict[slot]['example']))
    result = max(num)
    print(f'Max : {result}')
    return result

def check_redundunt(slots):
    s_names=[]
    flag = False
    for slot in slots:
        if guide_dict[slot]['name'] not in s_names:
            s_names.append(guide_dict[slot]['name'])
        else:
            flag = True
    print(f'Slots: {s_names} redundant state: {flag}')
    return flag

###########################################################################
#SLOT FILLING
excel_data = []
plus = ['ه','مون', 'م', 'ه؟', 'ها', 'ش', '!', 'ی', '،', '؟']
n = 1
i = 1
pattern_id = 0
for key, value in data_dict.items():
    sentence = value['tokenized']
    pattern_id = pattern_id + 1
    print(f'No : {i}')
    print(f'Question : {sentence}')
    print(f'len : {len(sentence)}')
    print(value['slots'])
    if value['slot'] == 1:
        if  len(sentence) <= 10:
            n = random.randint(3, 6)
            # print(f'choosen n = {n}')
            if (min_example_number(value['slots']) <= n <= max_example_number(value['slots'])) or n <min_example_number(value['slots']):
                pass
            else:
                # print('PROBLEM!')
                n = min_example_number(value['slots'])

        elif 11 < len(sentence) < 15:
            n = random.randint(2, 3)
            print(f'choosen n = {n}')
            if (min_example_number(value['slots']) <= n <= max_example_number(value['slots'])) or n <min_example_number(value['slots']):
                pass
            else:
                # print('PROBLEM!')
                n = min_example_number(value['slots'])
        else:
            n = 1
        print(f'Final n : {n}')
        slots = []
        for k in range(n):
            label = []
            new_sentence = []
            for w in sentence:
                print('Checking word in has slot ', w)
                if w in guide_dict:
                    print(f'{w} founded in guide')
                    examples = guide_dict[w]['example']
                    print(f'examples before shuffle: {examples}')
                    random.shuffle(examples)
                    print(f'examples after shuffle: {examples}')
                    # random_example = random.choice(examples)
                    print(f'choosen slot : {examples[0]}')
                    print(f'slots : {slots}')
                    random_example = examples[0]
                    if random_example in slots:
                        print(f'Duplicate found! : {random_example}')
                        if not check_redundunt(value['slots']):
                            while random_example in slots:
                                    random.shuffle(examples)
                                    random_example = examples[0]
                                    # min_example_number(value['slots'])
                                    # max_example_number(value['slots'])
                                    # print(f'len slots: {len(value["slots"])}')
                                    # print(n)
                                    # print(sentence)
                                    # print(slots)
                                    print(f'shuffled for {random_example}')
                    slots.append(random_example)
                    print(f'slots updated: {slots}')
                    preprocessed_example = preprocess(str(random_example))
                    name = guide_dict[w]['name']
                    print(f'Preprocessed example: ', preprocessed_example)
                    if len(preprocessed_example) == 1:
                        label.append('b-' + name)
                        new_sentence.append(preprocessed_example[0])
                    else:
                        for l in preprocessed_example:
                            if preprocessed_example.index(l) == 0:
                                print(f'for {l} {"b-" + name} added')
                                label.append('b-' + name)
                                new_sentence.append(l)
                            else:
                                print(f'for {l} {"i-" + name} added')
                                label.append('i-' + name)
                                new_sentence.append(l)
                    plus_list = {}
                    for p in plus:
                        if p in w:
                            print(f'from plus list {p} is found in {w}')
                            f = w[-1]
                            if f == p and len(w) < 3:
                                print('approved')
                                new_sentence.append(p)
                                label.append('o')

                else:
                    print(f'{w} not founded in guide go for O')
                    new_sentence.append(w)
                    label.append('o')
            print(new_sentence)
            print(len(new_sentence))
            print(label)
            print(len(label))
            print('*************************************')
            excel_data.append([i, pattern_id, " ".join(new_sentence), " ".join(label), value["Intent - Eng"]])
            i = i + 1
            # for index in range(len(new_sentence)):
            #     s = new_sentence[index]
            #     l = label[index]
            #     print(f'Adding row {s}  {l}')
            #     excel_data.append([s, l])


    else:
        print('Checking sentence in without slot go for O', sentence)
        label = []
        new_sentence = []
        for w in sentence:
            label.append('o')
            new_sentence.append(w)
        # print(new_sentence)
        # print(label)
        # print('######################################')
        excel_data.append([i, pattern_id, " ".join(new_sentence), " ".join(label), value["Intent - Eng"]])
        i = i + 1
        # for index in range(len(new_sentence)):
        #     s = new_sentence[index]
        #     l = label[index]
        #     print(f'Adding row {s}  {l}')
        #     excel_data.append([s, l])
        # excel_data.append([' ', '<s>'])
# print('**********************************************************************************************************')
# for row in excel_data:
#     print(row)


# Create a DataFrame from the excel_data list
df_excel = pd.DataFrame(excel_data, columns=['sample_id', 'pattern_id', 'text', 'slots', 'intent'])

# Save the DataFrame to an Excel file
excel_output_path = 'output-' + filename + '.xlsx'
df_excel.to_excel(excel_output_path, index=False)
