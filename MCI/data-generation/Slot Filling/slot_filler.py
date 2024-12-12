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
    for example_num in range(1, 13):
        example_key = f'example-{example_num}'
        example_value = row[example_key]
        if not pd.isna(example_value):
            guide_dict[shorten_value]['example'].append(example_value)

# LOADING DATA
# Load the Excel file into a DataFrame
excel_file_path_data = './data4.xlsx'
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

# CREATING DICTIONARY
# Preprocess the sample questions
normalizer = Normalizer()
stemmer = Stemmer()
preprocessed_sqs = []

for sq in sqs:
    # Normalize
    # normalized_sq = normalizer.normalize(sq)

    # Remove punctuation marks
    cleaned_sq = re.sub(r'[^\w\s]', '', sq)

    # Tokenize
    tokens = word_tokenize(cleaned_sq)

    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords_list()]

    # Stem
    # stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

    preprocessed_sqs.append(filtered_tokens)

# SLOT FINDING
new_sentences = []
# Define a function to recursively fill all combinations of slots
def fill_slots(sentence, tokens, token_index=0, filled_sentence="", n=1):
    if token_index >= len(tokens):
        # All slots are filled, print the filled sentence
        print(f'Filled sentence: {filled_sentence}')
        new_sentences.append(filled_sentence)
        return

    token = tokens[token_index]
    if token in guide_dict:
        t_data = guide_dict[token]
        examples = t_data['example']

        # Choose n random examples
        random_examples = random.sample(examples, n)
        if random_examples in sentence_tokens:
            while random_examples not in sentence_tokens:
                random_examples = random.sample(examples, n)
        # while random_examples not in sentence_tokens:
        #     random_examples = random.sample(examples, n)

        for random_example in random_examples:
            if type(random_example) == str or type(random_example) == int:
                if type(random_example) == int:
                    random_example = str(random_example)
                # Replace the token with the random example in a copy of the sentence
                new_sentence = sentence.replace(token, random_example)
                # print(f'New sentence: {new_sentence}')

                # Recursively fill the next token with the updated sentence
                fill_slots(new_sentence, tokens, token_index + 1, new_sentence, n)


# Prompt the user for the value of n
n = 1
result = {}
index = 0
# Check if each sentence has guide_dict keys
for sentence, sentence_tokens in zip(sqs, preprocessed_sqs):
    # print("Sentence:", sentence)
    result[index] = {}
    result[index]['original'] = sentence
    # print("sentence token: ", sentence_tokens)
    found_tokens = [token for token in sentence_tokens if token in guide_dict]
    if found_tokens:
        result[index]['slot'] = len(found_tokens)
        # print(f"{len(found_tokens)} Slot(s) Found:", found_tokens)

        # Start the recursive filling process
        fill_slots(sentence, found_tokens, n=n)
        new_s = new_sentences.pop()
        result[index]['new'] = new_s

    else:
        # print("No Slot")
        result[index]['slot'] = 0
    index = index + 1


def preprocess(sq):
    # Normalize
    # normalized_sq = normalizer.normalize(sq)

    # Remove punctuation marks
    cleaned_sq = re.sub(r'[^\w\s]', '', sq)

    # Tokenize
    tokens = word_tokenize(cleaned_sq)

    return tokens


excel_data = []


def slot_handler(col1, col2, col3, key):
    x_num = 0
    for r in col3:
        if r == 'x':
            x_num = x_num + 1
    if x_num == 1:
        if 'x' in col3:
            x_index = col3.index('x')
            if x_index < len(col1):
                s = col1[x_index]
                col3[x_index] = 'b-' + guide_dict[s]['name']
    elif x_num == result[key]['slot'] and x_num != 0:
        for t in col1:
            if t in guide_dict:
                rep_index = col1.index(t)
                if rep_index < len(col3):
                    col3[rep_index] = 'b-' + guide_dict[t]['name']
                rep_index = rep_index + 1
                while rep_index < len(col3) and col3[rep_index] != 'o':
                    col3[rep_index] = 'i-' + guide_dict[t]['name']
                    rep_index = rep_index + 1
    elif x_num != 0:
        for w in col1:
            if w in col2:
                if col2.index(w) < len(col3):
                    col3[col2.index(w)] = 'o'
            else:
                if w in guide_dict:
                    rep_index = col1.index(w)
                    if rep_index < len(col3):
                        col3[rep_index] = 'b-' + guide_dict[w]['name']
                    rep_index = rep_index + 1
                    while rep_index < len(col3) and col3[rep_index] != 'o':
                        col3[rep_index] = 'i-' + guide_dict[w]['name']
                        rep_index = rep_index + 1

    return col1, col2, col3


for key, value in result.items():
    col1 = preprocess(value['original'])
    col2 = []
    col3 = []
    if value['slot'] != 0:
        col2 = preprocess(value['new'])
        i = 0
        for row1, row2 in zip(col1, col2):
            if row1 == row2:
                col3.append('o')
            else:
                col3.append('x')
            i = i + 1
        # Handle cases where col2 is longer than col1
        while i < len(col2):
            col3.append('x')
            i = i + 1
        col1, col2, col3 = slot_handler(col1, col2, col3, key)
    else:
        for row in col1:
            col2.append(row)
            col3.append('o')
    # Append col2 and col3 to the excel_data list
    for word in col2:
        label = col3[col2.index(word)]
        excel_data.append([word,label])
    excel_data.append([' ','<s>'])


# Create a DataFrame from the excel_data list
df_excel = pd.DataFrame(excel_data, columns=['sentence', 'label'])

# Save the DataFrame to an Excel file
excel_output_path = 'output.xlsx'
df_excel.to_excel(excel_output_path, index=False)

