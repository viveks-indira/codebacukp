import xmlrpc.client
import random  # Ensure random is imported

# Odoo URL and database credentials
url = "https://crmindira-crm-22octstaging-16000205.dev.odoo.com"
db = "crmindira-crm-22octstaging-16000205"
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Connect to Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Retrieve leads assigned to different salespersons
salesperson_lead_ids = models.execute_kw(
    db, uid, password, 'crm.lead', 'search', [[('user_id', '!=', False)]]
)

# Check if there are leads with salespersons assigned
if salesperson_lead_ids:
    # Randomly select up to 200 leads
    lead_ids_to_update = random.sample(salesperson_lead_ids, min(200, len(salesperson_lead_ids)))

    # Define the values to update
    values = {
        'x_studio_current_week': 0,
        'x_studio_current_month': 50  # Set to the desired value
    }

    # Update the selected leads
    updated = models.execute_kw(db, uid, password, 'crm.lead', 'write', [lead_ids_to_update, values])

    if updated:
        print(f'Successfully updated {len(lead_ids_to_update)} lead(s) with random salespersons.')
    else:
        print('Failed to update leads.')
else:
    print('No leads found with assigned salespersons.')

print("done")
