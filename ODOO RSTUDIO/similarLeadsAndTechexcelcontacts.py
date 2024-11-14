import xmlrpc.client
import pandas as pd
from openpyxl import Workbook

# Odoo connection parameters
url = "https://crmindira.odoo.com"
db = "crmindira-crm-main-9343293"
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Connect to Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Fetch leads with partner_id not set and phone field set
leads = models.execute_kw(
    db, uid, password, 'crm.lead', 'search_read',
    [[['partner_id', '=', False], ['phone', '!=', False]]],
    {'fields': ['name', 'phone']}
)

# Function to normalize phone numbers
def normalize_phone(phone):
    phone = phone.replace('+91', '').strip()
    if len(phone) > 5:
        phone = phone[:5] + phone[5:].replace(' ', '')
    return phone

# Normalize phone numbers in leads
for lead in leads:
    lead['phone'] = normalize_phone(lead['phone'])

# Read Excel file
excel_file_path = r"C:\Users\freedom\Desktop\customer\updatedtechexcel.xlsx"
df = pd.read_excel(excel_file_path)

# Normalize phone numbers in Excel data
df['MOBILE_NO'] = df['MOBILE_NO'].astype(str).apply(normalize_phone)

# Compare and find matches
matched_records = []
for index, row in df.iterrows():
    for lead in leads:
        if row['CLIENT_NAME'] == lead['name'] and row['MOBILE_NO'] == lead['phone']:
            matched_records.append(row)

# Create a new Excel file with matched records
matched_df = pd.DataFrame(matched_records)
matched_file_path = r"C:\Users\freedom\Desktop\customer\matched_data.xlsx"
matched_df.to_excel(matched_file_path, index=False)

print(f'Matched records have been saved to {matched_file_path}')
