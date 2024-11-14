import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel(r"C:\Users\freedom\Desktop\Filter\Remaining.xlsx")

df=df.fillna('')
df.to_excel('Remaining.xlsx', index=False)

# Columns to apply the transformation
columns_to_replace = ['CLIENT_ID','CLIENT_NAME','MOBILE_NO','CLIENT_ID_MAIL','BIRTH_DATE','RESI_ADDRESS','CITY','STATE','PIN_CODE','COUNTRY','PAN_NO','RM_NAME','RM_CODE','REM_Code','TRADE_DATE']  # Replace with your column names

# Replace False values with empty strings for specific columns
for column in columns_to_replace:
    df[column] = df[column].apply(lambda x: '' if x is False else x)

# Save the modified DataFrame back to an Excel file if needed
df.to_excel('Remaining.xlsx', index=False)
