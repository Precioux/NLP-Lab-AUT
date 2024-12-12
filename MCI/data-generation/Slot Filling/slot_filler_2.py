import pandas as pd
from hazm import *
import re
import random

# LOADING GUIDE PART
# Load the Excel file into a DataFrame
excel_file_path = './guide.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Initialize an empty dictionary to store the key-value pairs
guide_dict = {}

# Iterate through the DataFrame rows and populate the dictionary
for index, row in df.iterrows():
    shorten_value = row['shorten value']

    # Create a dictionary for the current shorten_value if it doesn't exist
    if shorten_value not in guide_dict:
        guide_dict[shorten_value] = {}

    # Populate the dictionary for the current shorten_value
    guide_dict[shorten_value]['real value'] = row['real value']
    guide_dict[shorten_value]['name'] = row['name']
    guide_dict[shorten_value]['example'] = []
    # Collect all examples from columns 'example-1' to 'example-12'
    for example_num in range(1, 25):
        example_key = f'example-{example_num}'
        example_value = row[example_key]
        if not pd.isna(example_value):
            guide_dict[shorten_value]['example'].append(example_value)

#############################################################################################
# LOADING DATA
# Load the Excel file into a DataFrame
filename = 'data8'
excel_file_path_data = './'+filename+'.xlsx'
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
#################################################################################################
# CREATING DICTIONARY
# Preprocess the sample questions
result = {}
normalizer = Normalizer()
stemmer = Stemmer()
i = 0
for i, sq in enumerate(sqs):  # Use enumerate to keep track of the index
    # Normalize
    # normalized_sq = normalizer.normalize(sq)

    # Remove punctuation marks
    cleaned_sq = re.sub(r'[^\w\s]', '', sq)

    # Tokenize
    tokens = word_tokenize(cleaned_sq)

    # Store the result in the dictionary
    result[i] = {'original': tokens}

    if any(w in guide_dict for w in tokens):
        result[i]['slot'] = 1
    else:
        result[i]['slot'] = 0


def preprocess(sq):
    # Normalize
    # normalized_sq = normalizer.normalize(sq)

    # Remove punctuation marks
    cleaned_sq = re.sub(r'[^\w\s]', '', sq)

    # Tokenize
    tokens = word_tokenize(cleaned_sq)

    return tokens


###################################################################################################
# SLOT FILLING
excel_data = []
n = 1
for key, value in result.items():
    sentence = value['original']
    print(sentence)
    if value['slot'] == 1:
        for k in range(n):
            label = []
            new_sentence = []
            for w in sentence:
                print('Checking word in has slot ', w)
                if w in guide_dict:
                    print(f'{w} founded in guide')
                    examples = guide_dict[w]['example']
                    random_example = random.choice(examples)
                    if random_example in new_sentence:
                        while random_example not in new_sentence:
                            random_example = random.choice(examples)
                    preprocessed_example = preprocess(str(random_example))
                    name = guide_dict[w]['name']
                    print(f'Preprocessed example: ',preprocessed_example)
                    print(len(preprocessed_example))
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


                else:
                    print(f'{w} not founded in guide go for O')
                    new_sentence.append(w)
                    label.append('o')
            print(new_sentence)
            print(len(new_sentence))
            print(label)
            print(len(label))
            print('*************************************')

            for index in range(len(new_sentence)):
                s = new_sentence[index]
                l = label[index]
                print(f'Adding row {s}  {l}')
                excel_data.append([s, l])
            excel_data.append([' ', '<s>'])

    else:
        print('Checking sentence in without slot go for O',sentence)
        label = []
        new_sentence = []
        for w in sentence:
            label.append('o')
            new_sentence.append(w)
        # print(new_sentence)
        # print(label)
        # print('######################################')
        for index in range(len(new_sentence)):
            s = new_sentence[index]
            l = label[index]
            print(f'Adding row {s}  {l}')
            excel_data.append([s, l])
        excel_data.append([' ', '<s>'])

# Create a DataFrame from the excel_data list
df_excel = pd.DataFrame(excel_data, columns=['sentence', 'label'])

# Save the DataFrame to an Excel file
excel_output_path = 'output-'+filename+'.xlsx'
df_excel.to_excel(excel_output_path, index=False)


