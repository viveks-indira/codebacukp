import xmlrpc.client
import pandas as pd

url = 'https://crmindira.odoo.com'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'


# Connect to Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Fetch emails from Odoo mailing list with ID 29
mailing_list_id = 29
mailing_contacts = models.execute_kw(db, uid, password, 'mailing.contact', 'search_read', 
                                     [[('list_ids', 'in', [mailing_list_id])]], 
                                     {'fields': ['id','email']})
print(len(mailing_contacts))
# Read emails from Excel file
excel_file_path = r"C:\Users\freedom\Desktop\Indira Securities Pvt Ltd\12072024_data-1720845252198.xlsx"
df = pd.read_excel(excel_file_path)
excel_emails = df['Recipients'].tolist()  # Adjust column name as needed

# Create a list to store matching data
matched_data = []

# Compare emails and fetch data for matches
for contact in mailing_contacts:
    if contact['email'] in excel_emails:
        matched_data.append({
            'Recipients': contact['email'], 
        })

# Create a DataFrame from the matched data
matched_df = pd.DataFrame(matched_data)

# Save the matched data to a new Excel file
output_file_path = r"C:\Users\freedom\Desktop\Indira Securities Pvt Ltd\matchedfrodoo198.xlsx"
matched_df.to_excel(output_file_path, index=False)

print(f"Matched data has been saved to {output_file_path}")

