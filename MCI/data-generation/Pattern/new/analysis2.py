import pandas as pd

# Load the provided Excel file
file_path = 'data-coded.xlsx'
df = pd.read_excel(file_path)

# Rename columns for clarity
df = df.rename(columns={'label': 'intent_id', 'sentence': 'patterns'})

# Analyzing the data to get each intent's ID, number, patterns, and number of sentences
intent_analysis = df.groupby('intent').agg(
    Intent_ID=('intent_id', 'first'),
    Number_of_Patterns=('patterns', 'nunique'),
    Number_of_Sentences=('patterns', 'count')
).reset_index()

# Rename columns for clarity
intent_analysis = intent_analysis.rename(columns={
    'intent': 'Intent Name',
    'Intent_ID': 'Intent ID',
    'Number_of_Patterns': 'Number of Patterns',
    'Number_of_Sentences': 'Number of Sentences'
})

# Export the analysis to a new Excel file
output_path = 'intent_analysis_report.xlsx'
intent_analysis.to_excel(output_path, index=False)

print(f"Report generated and saved to {output_path}")
