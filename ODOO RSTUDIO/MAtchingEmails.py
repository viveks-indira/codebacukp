import pandas as pd
import xmlrpc.client

 
 
# Read Excel files
excel1 = pd.read_excel(r"C:\Users\freedom\Downloads\Mailing Contact (mailing.contact).xlsx")
excel2 = pd.read_excel(r"C:\Users\freedom\Downloads\12072024_data-1720845252198.xlsx")

# Extract relevant columns
emails1 = excel1['Email'].tolist()
recipients2 = excel2['Recipients'].tolist()
df1=pd.DataFrame(emails1)
df2=pd.DataFrame(recipients2)
# Find matches
matches = []
for email in emails1:
    if email in recipients2:
        matches.append(email)

# Create a DataFrame for the matches
matches_df = pd.DataFrame(matches, columns=['Matched Emails'])

# Export matches to a new Excel file
matches_df.to_excel(r'C:\Users\freedom\Downloads\matched_emails1.xlsx', index=False)

print("Matched emails have been exported to matched_emails1.xlsx")

