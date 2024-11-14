import xmlrpc.client
import pandas as pd

# Function to update partner_id in Odoo
def update_partner_id(odoo_client, db, uid, password, crm_lead_id, partner_name):
    models = xmlrpc.client.ServerProxy(odoo_client + '/xmlrpc/2/object')
    
    # Find partner_id in Odoo based on partner_name (CLIENT_NAME in updatedtech)
    partner_id = False
    partner_ids = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['name', '=', partner_name]]],
        {'limit': 1, 'fields': ['id']}
    )
    if partner_ids:
        partner_id = partner_ids[0]['id']
    
    if partner_id:
        models.execute_kw(db, uid, password, 'crm.lead', 'write', [[crm_lead_id], {'partner_id': partner_id}])
        print(f"Updated partner_id for CRM lead with id '{crm_lead_id}' to '{partner_name}'.")
    else:
        print(f"Partner '{partner_name}' not found in Odoo.")
# Odoo information
url = 'https://crmindira-crm-july-staging-14100614.dev.odoo.com/'
db = 'crmindira-crm-july-staging-14100614'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Read CRM leads data from Excel
crm_leads_file = r"C:\Users\freedom\Desktop\customer\crm_leads.xlsx"
df_crm_leads = pd.read_excel(crm_leads_file)

# Read updatedtech data from Excel
updatedtech_file = r"C:\Users\freedom\Desktop\customer\updatedtechexcel.xlsx"
df_updatedtech = pd.read_excel(updatedtech_file)


# Iterate through CRM leads and update partner_id if match found in updatedtech
for index, row in df_crm_leads.iterrows():
    crm_lead_id = row['id']
    crm_lead_name = row['name']
    crm_lead_phone = row['phone']
    
    found_match = False
    
    # Iterate through updatedtech DataFrame to find a match
    for index2, row2 in df_updatedtech.iterrows():
        if (row2['CLIENT_NAME'] == crm_lead_name) and (row2['MOBILE_NO'] == crm_lead_phone):
            found_match = True
            updated_name = row2['CLIENT_NAME']
            update_partner_id(odoo_client, db, uid, password, crm_lead_id, updated_name)
            break
    
    if not found_match:
      
        print(f"No updatedtech record found for CRM lead '{crm_lead_name}' with phone '{crm_lead_phone}'.")

print("Update process completed.")
