import pandas as pd
import re

def extract_phone_numbers(file_path, column_name, encoding='utf-8'):
    try:
        # Try reading the CSV file with the specified encoding
        df = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        # If there's a decoding error, try a different encoding
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

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

def save_to_csv(phone_numbers, output_file):
    # Convert the list of phone numbers to a DataFrame
    phone_numbers_df = pd.DataFrame(phone_numbers, columns=['Phone Number'])

    # Save the DataFrame to a CSV file
    phone_numbers_df.to_csv(output_file, index=False)

# Usage
file_path = 'path_to_your_file.csv'  # Replace with your CSV file path
column_name = 'your_column_name'     # Replace with the name of your column
output_file = 'extracted_phone_numbers.csv'  # Name of the output CSV file

phone_numbers = extract_phone_numbers(file_path, column_name)
save_to_csv(phone_numbers, output_file)

print(f'Extracted phone numbers saved to {output_file}')


"""Read the CSV file using Pandas.
Iterate through the rows of the specified column (you need to provide the column name).
Use a regular expression to find phone numbers that start with '353', '+353', '08', and their variants with or without spaces.
Extract and print or store these phone numbers."""
