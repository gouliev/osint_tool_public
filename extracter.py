import pandas as pd
import re

def extract_phone_numbers(file_path, column_name):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Regular expression for phone numbers
    phone_number_pattern = r'(\+?353\d{1,2}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3}|\b08\d{1}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3})'

    # List to store extracted phone numbers
    extracted_numbers = []

    # Iterate over each row in the column
    for number in df[column_name]:
        # Find all matches in the current row
        matches = re.findall(phone_number_pattern, str(number))
        extracted_numbers.extend(matches)

    return extracted_numbers

# Usage
file_path = 'path_to_your_file.csv'  # Replace with your CSV file path
column_name = 'your_column_name'     # Replace with the name of your column
phone_numbers = extract_phone_numbers(file_path, column_name)

# Print extracted phone numbers
for number in phone_numbers:
    print(number)

"""Read the CSV file using Pandas.
Iterate through the rows of the specified column (you need to provide the column name).
Use a regular expression to find phone numbers that start with '353', '+353', '08', and their variants with or without spaces.
Extract and print or store these phone numbers."""
