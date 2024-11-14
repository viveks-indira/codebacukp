import xmlrpc.client

# Connection details
url = 'https://crmindira-crm-22octstaging-16000205.dev.odoo.com//'
db = 'crmindira-crm-22octstaging-16000205'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Establish connection
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Define the filter details
model = "crm.lead"  # e.g., 'crm.lead'
user_id = 2                # The user ID for whom the filter is being created
domain = "[('user_id', '=', 257)]"  # Define your domain as a string

# Define filter data
filter_data = {
    'name': 'Escalated Test',
    'user_id': uid,  # Set the filter to be associated with the logged-in user
    'model_id': 'crm.lead',  # Replace with the model you want the filter for
    'domain': "[('user_id', '=', uid)]",  # Define the filter criteria
    'context': "{'is_favorite': True}"  # Mark as favorite
}

# Create the filter
try:
    filter_id = models.execute_kw(db, uid, password, 'ir.filters', 'create', [filter_data])
    print("Filter created with ID:", filter_id)
except xmlrpc.client.Fault as e:
    print("Error:", e)
print("Done")
