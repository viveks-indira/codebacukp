import pandas as pd
import xmlrpc.client
import numpy as np
from datetime import datetime
import re

# Odoo URL and database credentials
url = "https://crmindira-crm-22octstaging-16000205.dev.odoo.com"
db = "crmindira-crm-22octstaging-16000205"
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Connect to Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Connect to the object service
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


#Preparing the df to update and create contacts....................................................................................

#Fetch all the user ID's
user_data = models.execute_kw(db, uid, password,
    'res.users', 'search_read',[['|', ('active', '=', True), ('active', '=', False)]],  # Domain to fetch both active and inactive users
    {'fields': ['id', 'x_studio_rm_code_1']})

# Create DataFrame from the fetched data
df_users = pd.DataFrame(user_data)


# Fetch all states and their related countries
states = models.execute_kw(db, uid, password, 'res.country.state', 'search_read',[[]],{'fields': ['id', 'name', 'country_id']})

# Fetch all countries
countries = models.execute_kw(db, uid, password, 'res.country', 'search_read',[[]],{'fields': ['id', 'name']})

# Create DataFrames
df_states = pd.DataFrame(states)
df_countries = pd.DataFrame(countries)

# Rename columns for clarity
df_states.rename(columns={'id': 'state_id', 'name': 'state_name', 'country_id': 'country_id'}, inplace=True)
df_states = df_states.drop_duplicates(subset='state_name')
df_countries.rename(columns={'id': 'country_id', 'name': 'country_name'}, inplace=True)

# Convert names to lowercase for case-insensitive matching
df_states['state_name'] = df_states['state_name'].str.lower()
df_countries['country_name'] = df_countries['country_name'].str.lower()

# Load your Excel file into a DataFrame
df = pd.read_excel(r"E:\ODOO RSTUDIO\contact_update_formate.xlsx")
df = df.drop_duplicates("PAN_NO")

# Drop unwanted columns
#df_drop_unwanted = df.drop(['FIRST_NAME', 'LAST_NAME', 'MIDDLE_NAME', 'RESI_TEL_NO', 'Dealer_CODE', 'DEALER_NAME', 'REMESHIRE_GROUP', 'AGENTCODE', 'RELATIONSHIPOFFICER_CODE', 'INTRODUCER_CODE', 'MASTERPAN'], axis=1)
#df_drop_na = df_drop_unwanted.fillna('')
df_drop_na = df.fillna('')
# Fix date formats
def parse_date(date_str):
    if date_str is None or date_str == "NULL":
        return None  # Return None for NULL values

    try:
        if isinstance(date_str, str):
            # Check if the string is in MM/DD/YYYY format with time
            if '/' in date_str:
                try:
                    # Try parsing MM/DD/YYYY HH:MM:SS
                    parsed_date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                except ValueError:
                    try:
                        # Try parsing MM/DD/YYYY without time
                        parsed_date = datetime.strptime(date_str, '%m/%d/%Y')
                    except ValueError:
                        # Handle other string formats as needed
                        return None
                # Convert to the format YYYY-MM-DD HH:MM:SS
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                try:
                    # Handle ISO format with or without milliseconds
                    parsed_date = datetime.fromisoformat(date_str.split('.')[0])
                    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Handle other non-ISO formats if necessary
                    return None

        elif isinstance(date_str, datetime):
            # Already a datetime object, convert to string in YYYY-MM-DD HH:MM:SS format
            return date_str.strftime('%Y-%m-%d %H:%M:%S')

    except (ValueError, TypeError) as e:
        # Log or handle the error as appropriate
        print(f"Error parsing date: {e}")
        return None

      
      
df_drop_na['REGISTRATION_DATE'] = df_drop_na['REGISTRATION_DATE'].apply(parse_date)
df_drop_na['BIRTH_DATE'] = df_drop_na['BIRTH_DATE'].apply(parse_date)
df_drop_na['TRADE_DATE'] = df_drop_na['TRADE_DATE'].apply(parse_date)

# Remove .0 from mobile number and zip (pin code)
def remove_decimal_suffix(value):
    if isinstance(value, float):
        value = str(int(value))
    elif isinstance(value, str) and value.endswith('.0'):
        value = value[:-2]
    return value

df_drop_na['MOBILE_NO'] = df_drop_na['MOBILE_NO'].apply(remove_decimal_suffix)
df_drop_na['PIN_CODE'] = df_drop_na['PIN_CODE'].apply(remove_decimal_suffix)

# Helper function to normalize phone numbers (remove country code and spaces)
def normalize_phone(phone):
    phone = str(phone)
    return re.sub(r'\D', '', phone[-10:])

# Helper function to sanitize data to handle XML-RPC limits
def sanitize_data(data):
    for key, value in data.items():
        # Convert integers that exceed XML-RPC limits to strings
        if isinstance(value, int) and (value > 2**31 - 1 or value < -2**31):
            data[key] = str(value)
        # Handle dates and other specific cases
        if key in ['x_studio_last_trade', 'x_studio_date_of_birth'] and value in [None, '']:
            data[key] = False
    return data
  
# Ensure 'STATE' and 'COUNTRY' columns are in lower case for mapping
df_drop_na['STATE'] = df_drop_na['STATE'].str.lower()
df_drop_na['COUNTRY'] = df_drop_na['COUNTRY'].str.lower()

# Map state and country names to IDs
df_drop_na['state_id'] = df_drop_na['STATE'].map(df_states.set_index('state_name')['state_id']).fillna('')
df_drop_na['state_id'] = df_drop_na['state_id'].astype(int, errors='ignore')

df_drop_na['country_id'] = df_drop_na['COUNTRY'].map(df_countries.set_index('country_name')['country_id']).fillna('')
df_drop_na['country_id'] = df_drop_na['country_id'].astype(int, errors='ignore')

# Drop the original STATE and COUNTRY columns
df_drop_na.drop(['STATE', 'COUNTRY'], axis=1, inplace=True)

#Find ID of RM's in Odoo
df_drop_na = pd.merge(df_drop_na, df_users, how='left', left_on='RELATIONMANAGER_CODE', right_on='x_studio_rm_code_1')
df_drop_na = df_drop_na.rename(columns={'id': 'user_id'})

default_user_id = 2  # or any other placeholder value
df_drop_na['user_id'] = df_drop_na['user_id'].fillna(default_user_id)


# DataFrames for existing and new contacts
existing_contacts = []
new_contacts = []

# Iterate over each row in the DataFrame
for index, row in df_drop_na.iterrows():
    name = row['CLIENT_NAME']
    phone = row['MOBILE_NO']
    normalized_phone = normalize_phone(phone)

    # Search for the contact by name (case insensitive) and normalized phone
    contacts = models.execute_kw(db, uid, password, 'res.partner', 'search_read',[[('name', 'ilike', name)]], {'fields': ['id', 'name', 'x_studio_phone1']})

    contact_found = False
    for contact in contacts:
        contact_phone = normalize_phone(contact['x_studio_phone1'] or '')
        if contact_phone == normalized_phone:
            existing_contacts.append((contact['id'], row))
            contact_found = True
            break
    
    if not contact_found:
        new_contacts.append(row)

# Create DataFrames for existing and new contacts
df_existing_contacts = pd.DataFrame(existing_contacts, columns=['id', 'data'])
df_new_contacts = pd.DataFrame(new_contacts)

print(f'Found {len(df_existing_contacts)} existing contacts.')
print(f'Found {len(df_new_contacts)} new contacts.')

df_existing_contacts.to_excel(r"E:\ODOO RSTUDIO\existing_clients_df_after_fix.xlsx")
df_new_contacts.to_excel(r"E:\ODOO RSTUDIO\new_contacts_df_after_fix.xlsx")
df_drop_na.to_excel(r"E:\ODOO RSTUDIO\prepared_df_before_splitting_after_fix_1.xlsx")
#Updating contacts................................................................................................


# Update existing contacts
for index, row in df_existing_contacts.iterrows():
    contact_id = row['id']
    contact_data = row['data']

    # Prepare the data to update
    contact_update_data = {
        'name': contact_data['CLIENT_NAME'],
        'x_studio_display_name': contact_data['CLIENT_NAME'],
        'x_studio_client_id_1': contact_data['CLIENT_ID'],
        'street': contact_data['RESI_ADDRESS'],
        'city': contact_data['CITY'],
        'zip': contact_data['PIN_CODE'],
        'state_id': contact_data.get('state_id', False),
        'country_id': contact_data.get('country_id', False),
        'x_studio_pan_no': contact_data['PAN_NO'],
        'email': contact_data['CLIENT_ID_MAIL'],
        'x_studio_phone1': contact_data['MOBILE_NO'],
        'x_studio_rm_name': contact_data['RM_NAME'],
        'x_studio_rm_code': contact_data['RELATIONMANAGER_CODE'],
        'x_studio_remisher_code': contact_data['REM_CODE'],
        'x_studio_last_trade': contact_data['TRADE_DATE'],
        'x_studio_date_of_birth': contact_data['BIRTH_DATE'],
    }

    # Sanitize the data
    contact_update_data['user_id'] = int(contact_data['user_id'])
    contact_update_data = sanitize_data(contact_update_data)
    
    # Update the existing contact
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[contact_id], contact_update_data])
    print(f'Updated contact: {contact_data["CLIENT_NAME"]} ({contact_data["MOBILE_NO"]})')


#Creating new contacts..................................................................................................

# Create new contacts
new_contacts_data = []
newly_created_contacts = []

for index, row in df_new_contacts.iterrows():
    contact_data = {
        'name': row['CLIENT_NAME'],
        'x_studio_display_name': row['CLIENT_NAME'],
        'x_studio_client_id_1': row['CLIENT_ID'],
        'street': row['RESI_ADDRESS'],
        'city': row['CITY'],
        'zip': row['PIN_CODE'],
        'state_id': row.get('state_id', False),
        'country_id': row.get('country_id', False),
        'x_studio_pan_no': row['PAN_NO'],
        'email': row['CLIENT_ID_MAIL'],
        'x_studio_phone1': row['MOBILE_NO'],
        'x_studio_rm_name': row['RM_NAME'],
        'x_studio_rm_code': row['RELATIONMANAGER_CODE'],
        'x_studio_remisher_code': row['REM_CODE'],
        'x_studio_last_trade': row['TRADE_DATE'],
        'x_studio_date_of_birth': row['BIRTH_DATE'],
    }
    
    # Sanitize the data
    #contact_data['user_id'] = int(row['user_id'])
    contact_data = sanitize_data(contact_data)
    
    new_contacts_data.append(contact_data)

# Batch create new contacts
if new_contacts_data:
    #newly_created_contacts = models.execute_kw(db, uid, password, 'res.partner', 'create', [new_contacts_data])
    models.execute_kw(db, uid, password, 'res.partner', 'create', [new_contacts_data])
print(f'Created {len(new_contacts_data)} new contacts.')


#fetching id of newly created contacts to create new leads
#df_newly_created_contacts = pd.DataFrame(new_contacts_data)
#df_newly_created_contacts['id'] = newly_created_contacts


#Preparing the df to update and create leads....................................................................................


# Iterate through leads_of_existing_contacts and update the leads and create new leads
for index, row in df_drop_na.iterrows():
    client_name = row['CLIENT_NAME']
    mobile_no = normalize_phone(row['MOBILE_NO'])
    
    # Search for the existing lead based on partner_id and phone
    partner_ids = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[
        ('name', 'ilike', client_name),
    ], ['id', 'name', 'x_studio_phone1']])
    
    partner_id = False
    for partner in partner_ids:
        normalized_partner_phone = normalize_phone(partner['x_studio_phone1'])
        if normalized_partner_phone == mobile_no:
            partner_id = partner['id']
            break

    if partner_id:
        lead_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search', [[
            ('partner_id', '=', partner_id),
            ('phone', 'like', mobile_no)
        ]])
        
        # If the lead exists, update it with the new values from df_existing_contacts
        if lead_ids:
            lead_id = lead_ids[0]
            update_values = {
                'name': client_name,
                'user_id': int(row['user_id']),
                'street': row['RESI_ADDRESS'],
                'city': row['CITY'],
                'zip': row['PIN_CODE'],
                'state_id': row.get('state_id', False),
                'country_id': row.get('country_id', False),
                'x_studio_rm_source': row['RELATIONMANAGER_CODE'],
                'x_studio_rem_code': row['REM_CODE'],
            }
            # Sanitize the data before updating
            update_values = sanitize_data(update_values)
            models.execute_kw(db, uid, password, 'crm.lead', 'write', [[lead_id], update_values])
            print(f'Updated lead: CLIENT_NAME={client_name}')
        
        else:
            # Create a new lead if no existing lead found
            new_lead_values = {
                'name': client_name,
                'partner_id': partner_id,
                'user_id': int(row['user_id']),
                'street': row['RESI_ADDRESS'],
                'city': row['CITY'],
                'zip': row['PIN_CODE'],
                'state_id': row.get('state_id', False),
                'country_id': row.get('country_id', False),
                'x_studio_rm_source': row['RELATIONMANAGER_CODE'],
                'x_studio_rem_code': row['REM_CODE'],
                'x_studio_lead_type': 'Trading',
                'x_studio_communication_type': 'Calling',
                'x_studio_client_response': 'Interested',
                'x_studio_account_type': 'Client',
            }
            # Sanitize the data before creating
            new_lead_values = sanitize_data(new_lead_values)
            models.execute_kw(db, uid, password, 'crm.lead', 'create', [new_lead_values])
            print(f'Created new lead: CLIENT_NAME={client_name}')
    
    else:
        print(f'No matching partner found for CLIENT_NAME={client_name}')

print("Code completely executed")

print("Lead upload in process....")
print("done")
