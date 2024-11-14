import pandas as pd
from odoo import models, fields, api
import xmlrpc.client

url = 'https://crmindira.odoo.com'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'
# Connect to Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Fetch contact records from Odoo
contacts = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['x_studio_client_id_1', '!=', False]]], {'fields': ['id', 'x_studio_client_id_1']})

# Create a dictionary of Odoo client IDs
odoo_client_ids = {str(contact['x_studio_client_id_1']): contact['id'] for contact in contacts}

# Read the Excel file
df = pd.read_excel(r"C:\Users\freedom\Downloads\total Client list 9-7-24.xlsx")

# Normalize the client IDs to strings for comparison
df['CLIENT_ID'] = df['CLIENT_ID'].astype(str)

# Find records where CLIENT_ID does not match Odoo x_studio_client_id_1
non_matching_records = df[~df['CLIENT_ID'].isin(odoo_client_ids.keys())]

# Save the non-matching records to a new Excel file
non_matching_records.to_excel(r"C:\Users\freedom\Downloads\non_matching_records.xlsx", index=False)

print("Non-matching records have been saved to 'non_matching_records.xlsx'.")
