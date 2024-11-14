import xmlrpc.client
import pandas as pd

url = 'https://crmindira-crm-main-9343293.dev.odoo.com/'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'


# Common endpoint
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Object endpoint
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Lead IDs to update
lead_ids = [164359, 2639, 2569, 61105, 60830, 79013, 164563]

# Salesperson ID to set (ISPL user ID is 2)
salesperson_id = 2

# Update each lead individually
for lead_id in lead_ids:
    result = models.execute_kw(db, uid, password, 'crm.lead', 'write', [[lead_id], {
        'user_id': salesperson_id
    }])
    
    if result:
        print(f"Salesperson updated successfully for lead ID: {lead_id}")
    else:
        print(f"Failed to update lead ID: {lead_id}")
        
print("Done")        
        
