import pandas as pd

# Path to the original Excel file
input_file_path = r"C:\Users\freedom\Downloads\matched_emails.xlsx"

# Path to save the new Excel file without duplicates
output_file_path = r"C:\Users\freedom\Downloads\cleaned_file.xlsx"

# Read the Excel file
df = pd.read_excel(input_file_path)

# Remove duplicates
df_cleaned = df.drop_duplicates()

# Export the cleaned DataFrame to a new Excel file
df_cleaned.to_excel(output_file_path, index=False)

print("Duplicates have been removed and cleaned data is saved to cleaned_file.xlsx.")
