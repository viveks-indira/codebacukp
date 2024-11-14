import pandas as pd

# Load the Excel file
file_path = r"C:\Users\freedom\Desktop\Filter\filtered_data_with_r_d (1).xlsx"
df = pd.read_excel(file_path)

# Remove empty rows
df_cleaned = df.dropna(how='all')

# Save the cleaned DataFrame back to an Excel file
cleaned_file_path = r"C:\Users\freedom\Desktop\Filter\filtered.xlsx"
df_cleaned.to_excel(cleaned_file_path, index=False)

print(f"Cleaned file saved at: {cleaned_file_path}")
