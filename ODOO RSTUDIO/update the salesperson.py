import xmlrpc.client
import pandas as pd

url = 'https://crmindira-crm-19julystaging-14299297.dev.odoo.com/'
db = 'crmindira-crm-19julystaging-14299297'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Object endpoint
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Load the Excel file
input_file = r"C:\Users\freedom\Downloads\rmname.xlsx"  # Replace with your input Excel file
df = pd.read_excel(input_file)

# Salesperson ID to set (ISPL user ID is 2)
salesperson_id = 8

# Field names
client_id_field = 'x_studio_client_id_1'  # Correct field name for Client ID in Odoo

# Update each lead based on Client ID from Excel
for client_id in df['Client ID']:
    # Search for the lead based on Client ID
    lead_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search', [[(client_id_field, '=', client_id)]])
    
    if lead_ids:
        # Update the salesperson for each lead found
        result = models.execute_kw(db, uid, password, 'crm.lead', 'write', [lead_ids, {
            'user_id': salesperson_id
        }])
        
        if result:
            print(f"Salesperson updated successfully for Client ID: {client_id}")
        else:
            print(f"Failed to update Client ID: {client_id}")
    else:
        print(f"No lead found for Client ID: {client_id}")

print("Done")
