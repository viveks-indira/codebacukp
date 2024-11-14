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

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Connect to the object service
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Preparing the DataFrame to update and create contacts
# Fetch all the user IDs
user_data = models.execute_kw(db, uid, password,
    'res.users', 'search_read',[['|', ('active', '=', True), ('active', '=', False)]],  # Domain to fetch both active and inactive users
    {'fields': ['id', 'x_studio_rm_code_1']})

# Create DataFrame from the fetched data
df_users = pd.DataFrame(user_data)

# Fetch all states and their related countries
states = models.execute_kw(db, uid, password, 'res.country.state', 'search_read',[[]],{'fields': ['id', 'name', 'country_id']})
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

# Fill NA values
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
                    parsed_date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                except ValueError:
                    try:
                        parsed_date = datetime.strptime(date_str, '%m/%d/%Y')
                    except ValueError:
                        return None
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                try:
                    parsed_date = datetime.fromisoformat(date_str.split('.')[0])
                    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return None
        elif isinstance(date_str, datetime):
            return date_str.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError) as e:
        print(f"Error parsing date: {e}")
        return None

df_drop_na['REGISTRATION_DATE'] = df_drop_na['REGISTRATION_DATE'].apply(parse_date)
df_drop_na['BIRTH_DATE'] = df_drop_na['BIRTH_DATE'].apply(parse_date)
df_drop_na['TRADE_DATE'] = df_drop_na['TRADE_DATE'].apply(parse_date)

# Remove decimal suffix from mobile number and PIN code
def remove_decimal_suffix(value):
    if isinstance(value, float):
        value = str(int(value))
    elif isinstance(value, str) and value.endswith('.0'):
        value = value[:-2]
    return value

df_drop_na['MOBILE_NO'] = df_drop_na['MOBILE_NO'].apply(remove_decimal_suffix)
df_drop_na['PIN_CODE'] = df_drop_na['PIN_CODE'].apply(remove_decimal_suffix)

# Helper function to normalize phone numbers
def normalize_phone(phone):
    phone = str(phone)
    return re.sub(r'\D', '', phone[-10:])

# Helper function to sanitize data
def sanitize_data(data):
    for key, value in data.items():
        if isinstance(value, int) and (value > 2**31 - 1 or value < -2**31):
            data[key] = str(value)
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

# Find ID of RM's in Odoo
df_drop_na = pd.merge(df_drop_na, df_users, how='left', left_on='RELATIONMANAGER_CODE', right_on='x_studio_rm_code_1')
df_drop_na = df_drop_na.rename(columns={'id': 'user_id'})

default_user_id = 2  # Placeholder value
df_drop_na['user_id'] = df_drop_na['user_id'].fillna(default_user_id)

# DataFrames for existing and new contacts
existing_contacts = []
new_contacts = []

# Iterate over each row in the DataFrame
for index, row in df_drop_na.iterrows():
    name = row['CLIENT_NAME']
    phone = row['MOBILE_NO']
    normalized_phone = normalize_phone(phone)

    # Search for the contact by name and normalized phone
    contacts = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[('name', 'ilike', name)]], {'fields': ['id', 'name', 'x_studio_phone1']})

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

# Updating contacts
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

# Creating new contacts
for index, row in df_new_contacts.iterrows():
    new_contact_data = {
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
        'user_id': int(row['user_id']),  # Assigning the user_id from earlier mapping
    }

    # Sanitize the new contact data
    new_contact_data = sanitize_data(new_contact_data)

    # Create the new contact
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [new_contact_data])
    print(f'Created new contact: {row["CLIENT_NAME"]} ({row["MOBILE_NO"]})')

print("Process completed.")
