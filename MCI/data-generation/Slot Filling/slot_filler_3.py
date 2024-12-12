import pandas as pd
from hazm import *
import re
import random
import openpyxl

# LOADING GUIDE PART
# Load the Excel file into a DataFrame
excel_file_path = './guide.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
guide_dict = {}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in df.iterrows():
    shorten_value = row['shorten value']
    if type(shorten_value) == str:
        print('Not null')
        shorten_value1 = row['shorten value'] + '؟'
        shorten_value2 = row['shorten value'] + 'ش'
        shorten_value3 = row['shorten value'] + 'ها'
        shorten_value4 = row['shorten value'] + '!'
        shorten_value5 = row['shorten value'] + 'ی'
        shorten_value6 = row['shorten value'] + '،'
        shorten_value7 = row['shorten value'] + 'ه'
        shorten_value8 = row['shorten value'] + 'م'
        shorten_value9 = row['shorten value'] + 'ه؟'
        shorten_value9 = row['shorten value'] + 'مون'

        # Create a dictionary for the current shorten_value if it doesn't exist
        if shorten_value not in guide_dict:
            guide_dict[shorten_value] = {}
        if shorten_value1 not in guide_dict:
            guide_dict[shorten_value1] = {}
        if shorten_value2 not in guide_dict:
            guide_dict[shorten_value2] = {}
        if shorten_value3 not in guide_dict:
            guide_dict[shorten_value3] = {}
        if shorten_value4 not in guide_dict:
            guide_dict[shorten_value4] = {}
        if shorten_value5 not in guide_dict:
            guide_dict[shorten_value5] = {}
        if shorten_value6 not in guide_dict:
            guide_dict[shorten_value6] = {}
        if shorten_value7 not in guide_dict:
            guide_dict[shorten_value7] = {}
        if shorten_value8 not in guide_dict:
            guide_dict[shorten_value8] = {}
        if shorten_value9 not in guide_dict:
            guide_dict[shorten_value9] = {}

        # Populate the dictionary for the current shorten_value
        guide_dict[shorten_value]['real value'] = row['real value']
        guide_dict[shorten_value]['name'] = row['name']
        guide_dict[shorten_value]['example'] = []
        guide_dict[shorten_value1]['real value'] = row['real value']
        guide_dict[shorten_value1]['name'] = row['name']
        guide_dict[shorten_value1]['example'] = []
        guide_dict[shorten_value2]['real value'] = row['real value']
        guide_dict[shorten_value2]['name'] = row['name']
        guide_dict[shorten_value2]['example'] = []
        guide_dict[shorten_value3]['real value'] = row['real value']
        guide_dict[shorten_value3]['name'] = row['name']
        guide_dict[shorten_value3]['example'] = []
        guide_dict[shorten_value4]['real value'] = row['real value']
        guide_dict[shorten_value4]['name'] = row['name']
        guide_dict[shorten_value4]['example'] = []
        guide_dict[shorten_value5]['name'] = row['name']
        guide_dict[shorten_value5]['example'] = []
        guide_dict[shorten_value6]['name'] = row['name']
        guide_dict[shorten_value6]['example'] = []
        guide_dict[shorten_value7]['name'] = row['name']
        guide_dict[shorten_value7]['example'] = []
        guide_dict[shorten_value8]['name'] = row['name']
        guide_dict[shorten_value8]['example'] = []
        guide_dict[shorten_value9]['name'] = row['name']
        guide_dict[shorten_value9]['example'] = []

        # Collect all examples from columns 'example-1' to 'example-12'
        for example_num in range(1, 109):
            example_key = f'example-{example_num}'
            example_value = row[example_key]
            if not pd.isna(example_value):
                guide_dict[shorten_value]['example'].append(example_value)
                guide_dict[shorten_value1]['example'].append(example_value)
                guide_dict[shorten_value2]['example'].append(example_value)
                guide_dict[shorten_value3]['example'].append(example_value)
                guide_dict[shorten_value4]['example'].append(example_value)
                guide_dict[shorten_value5]['example'].append(example_value)
                guide_dict[shorten_value6]['example'].append(example_value)
                guide_dict[shorten_value7]['example'].append(example_value)
                guide_dict[shorten_value8]['example'].append(example_value)
                guide_dict[shorten_value9]['example'].append(example_value)

# for key,value in guide_dict.items():
#     print(key)
#     print(value)
#############################################################################################
# LOADING DATA
# Load the Excel file into a DataFrame
filename = ('data_new_input')
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
            'No': row['No'],
            'Domain - Per': row['Domain - Per'],
            'Domain - Eng': row['Domain - Eng'],
            'Intent - Per': row['Intent - Per'],
            'Intent - Eng': row['Intent - Eng']
        }

# #################################################################################################
# CREATING DICTIONARY
# Preprocess the sample questions
normalizer = Normalizer()
stemmer = Stemmer()
for key, value in data_dict.items():
    # Tokenize
    tokens = key.split()

    # Store the result in the dictionary
    value['tokenized'] = tokens

    if any(w in guide_dict for w in tokens):
        value['slot'] = 1
    else:
        value['slot'] = 0


def preprocess(sq):
    # Tokenize
    tokens = sq.split()

    return tokens


# # ###################################################################################################
# # SLOT FILLING
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
    if value['slot'] == 1:
        if  len(sentence) < 10:
            # n=1
            n = random.randint(3, 6)
        elif 11 < len(sentence) < 15:
            # n=1
            n = random.randint(2,3)
        else:
            n = 1
        print(f'n : {n}')
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
                        print('Duplicate found!')
                        if len(examples) > 10:
                            while random_example in slots:
                                random.shuffle(examples)
                                random_example = examples[0]
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
