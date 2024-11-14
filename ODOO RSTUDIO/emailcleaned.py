import xmlrpc.client
import pandas as pd

#url = 'https://crmindira-crm-19julystaging-14299297.dev.odoo.com/'
#db = 'crmindira-crm-19julystaging-14299297'
#username = 'sharshit@indiratrade.com'
#password = 'Crm@123'

url = 'https://crmindira.odoo.com/'
db = 'crmindira-crm-main-9343293'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Define model and fields
model_mailing_contact = 'mailing.contact'
field_name = 'email'

# Fetch contacts for the given mailing list ID
mailing_list_id = 29

# Search for contact IDs belonging to the mailing list
contact_ids = models.execute_kw(db, uid, password,
    model_mailing_contact, 'search',
    [[('list_ids', 'in', mailing_list_id)]])

# Read the email addresses of the contacts
emails = models.execute_kw(db, uid, password,
    model_mailing_contact, 'read',
    [contact_ids, [field_name]])

# Extract the email addresses
email_list = [contact[field_name] for contact in emails]
df_maillist = pd.DataFrame(email_list, columns=['Email'])

# Create a DataFrame from the email list
odoo_df = pd.DataFrame(email_list, columns=['Email'])

# Load the Excel file
excel_df = pd.read_excel(r"C:\Users\freedom\Desktop\Odoo\8_8_2024\remove.xlsx")


# Convert both email columns to lowercase to avoid case mismatch
odoo_df['Email'] = odoo_df['Email'].str.lower()
excel_df['Email'] = excel_df['Email'].str.lower()

# Find matching emails
matches = excel_df[excel_df['Email'].isin(odoo_df['Email'])]

# Count the matches
match_count = matches.shape[0]

print(f"\nNumber of matching emails: {match_count}")

# Print matching emails
#if match_count > 0:
#    print("\nMatching emails:")
#    for match in matches['Email']:
#        print(match)
#else:
#    print("No matching emails found.")
    
    
    

# Delete the matching records
if match_count > 0:
    # Identify the contact IDs to delete
    emails_to_delete = matches['Email'].tolist()

    # Search for the contact IDs to delete in Odoo
    contact_ids_to_delete = models.execute_kw(db, uid, password,
        model_mailing_contact, 'search',
        [[('email', 'in', emails_to_delete), ('list_ids', 'in', mailing_list_id)]])

    # Delete the contacts
    if contact_ids_to_delete:
        models.execute_kw(db, uid, password,
            model_mailing_contact, 'unlink',
            [contact_ids_to_delete])
        
        print(f"Deleted {len(contact_ids_to_delete)} contacts from the mailing list.")
else:
    print("No matching emails found.")
