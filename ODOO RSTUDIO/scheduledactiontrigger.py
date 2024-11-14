import xmlrpc.client
import pandas as pd

url = "https://crmindira-crm-19julystaging-14299297.dev.odoo.com/"
db = "crmindira-crm-19julystaging-14299297"
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Login and authenticate
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Connect to the Odoo model
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


try:
    # Retrieve all scheduled actions
    scheduled_actions = models.execute_kw(
        db, uid, password, 'ir.cron', 'search_read',
        [[], ['id', 'name', 'nextcall', 'state', 'active', 'model_id', 'code']]
    )
    
    # Create a DataFrame from the fetched scheduled actions
    df_scheduled_actions = pd.DataFrame(scheduled_actions)

    # Print the DataFrame
    print(df_scheduled_actions)
    action_id = 93
    result = models.execute_kw(db, uid, password, 'ir.cron', 'method_direct_trigger', [action_id])

    print(f"Scheduled action ID {action_id} executed successfully: {result}")

except xmlrpc.client.Fault as e:
    print(f"Error fetching scheduled actions: {e}")

print("done")




all_users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[], ['id', 'partner_id']])

# Find the scheduled action with ID 93
scheduled_action_id = models.execute_kw(
    db, uid, password, 'ir.cron', 'search',
    [[('id', '=', 93)]]
)

# Execute the scheduled action (if found)
if scheduled_action_id:
    try:
        result = models.execute_kw(
            db, uid, password, 'ir.cron', 'method_direct_trigger',
            [scheduled_action_id]
        )
        print(f"Scheduled action with ID 93 triggered successfully.")
    except xmlrpc.client.Fault as e:
        print(f"Error triggering scheduled action: {e}")
else:
    print("Scheduled action with ID 93 not found.")
print("done")
