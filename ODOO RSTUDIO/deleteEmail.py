import xmlrpc.client
import pandas as pd

url = 'https://crmindira.odoo.com'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Odoo XML-RPC models
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Excel file path
excel_file = r"C:\Users\freedom\Downloads\filtered400email615.xlsx"

# Model and field information
model = 'mailing.contact'
field_name = 'email'
excel_column_name = 'Recipients'

# Read Excel file into pandas DataFrame
df1 = pd.read_excel(excel_file)
df1.to_excel("Crosscheck.xlsx")
# Get list of emails from Excel and convert to strings
emails_to_delete = df1[excel_column_name].astype(str).tolist()

# Retrieve records from Odoo based on the mailing list ID
mailing_list_id = 29  # Change this to your specific mailing list ID
records = models.execute_kw(db, uid, password, model, 'search_read', [[('list_ids', 'in', [mailing_list_id])]], {'fields': ['id', field_name]})

# Convert Odoo emails to strings and store in DataFrame
df2 = pd.DataFrame(records)
df2[field_name] = df2[field_name].astype(str)

# Delete records where email matches
for record in records:
    if str(record[field_name]) in emails_to_delete:
        # Delete record
        models.execute_kw(db, uid, password, model, 'unlink', [[record['id']]])
        

print("Deletion process completed.")
