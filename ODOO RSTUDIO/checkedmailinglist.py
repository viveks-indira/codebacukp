import xmlrpc.client

url = 'https://crmindira.odoo.com'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'


# XMLRPC endpoint paths
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Authenticate and obtain UID
uid = common.authenticate(db, username, password, {})

# ID of the specific mailing list you want to fetch data for
mailing_list_id = 29

# Fetching mailing list name
model_name = 'mailing.list'
mailing_list = models.execute_kw(db, uid, password, model_name, 'read', [mailing_list_id], {'fields': ['id', 'name']})

# Print mailing list name
print("Mailing List:")
print("ID: {}, Name: {}".format(mailing_list['id'], mailing_list['name']))
