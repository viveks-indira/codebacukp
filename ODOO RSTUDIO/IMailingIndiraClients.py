import xmlrpc.client
import pandas as pd


# Authenticate and connect to Odoo via XML-RPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# ID of the specific mailing list you want to fetch data for
mailing_list_id = 23

# Fetching mailing list name
model_name = 'mailing.list'
mailing_list = models.execute_kw(db, uid, password, model_name, 'read', [mailing_list_id], {'fields': ['id', 'name']})

# Print mailing list name
print("Mailing List:")
print("ID: {}, Name: {}".format(mailing_list['id'], mailing_list['name']))

# Read emails from Excel file
excel_file = r"C:\Users\freedom\Downloads\Sheet1.xlsx"
df = pd.read_excel(excel_file)

# Fetch recipients from Excel file
recipients_to_insert = df['Recipients'].tolist()

# Fetch records inside the mailing list matching recipients
record_model_name = 'mailing.contact'
matched_records = []

for recipient in recipients_to_insert:
    record_ids = models.execute_kw(db, uid, password, record_model_name, 'search', [[('list_ids', 'in', [mailing_list_id]), ('email', '=', recipient)]])
    if record_ids:
        records = models.execute_kw(db, uid, password, record_model_name, 'read', [record_ids], {'fields': ['id', 'name', 'email']})
        matched_records.extend(records)

# Print matched records
if matched_records:
    print("Matched Records to Insert into Mailing List {}: ".format(mailing_list['name']))
    matched_df = pd.DataFrame(matched_records)
    print(matched_df)
else:
    print("No matching records found.")

# Optionally, insert matched records into a DataFrame
# matched_df = pd.DataFrame(matched_records)

print("Process completed.")
