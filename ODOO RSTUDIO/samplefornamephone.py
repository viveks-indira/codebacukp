import xmlrpc.client
import pandas as pd


# Function to remove +91 prefix and spaces from phone numbers
def clean_phone_number(phone_number):
    if pd.isna(phone_number):
        return phone_number
    elif isinstance(phone_number, str):
        cleaned_number = phone_number.replace('+91', '').replace(' ', '')
        return cleaned_number
    else:
        return phone_number

# Function to convert input to string
def to_str(value):
    if pd.isna(value):
        return ''
    return str(value)

# XML-RPC connection setup
url = 'https://crmindira-crm-july-staging-14100614.dev.odoo.com/'
db = 'crmindira-crm-july-staging-14100614'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Read 'updatedtech' Excel file
excel_file = r"C:\Users\freedom\Desktop\customer\updatedtechexcel.xlsx"
try:
    df_updatedtech = pd.read_excel(excel_file)
    
    # Convert CLIENT_NAME and MOBILE_NO to strings
    df_updatedtech['CLIENT_NAME'] = df_updatedtech['CLIENT_NAME'].apply(to_str)
    df_updatedtech['MOBILE_NO'] = df_updatedtech['MOBILE_NO'].apply(clean_phone_number)
    
except Exception as e:
    print(f"Error reading Excel file: {e}")
    df_updatedtech = pd.DataFrame()  # Empty DataFrame if read fails

# Ensure column names are correct and accessible
if 'CLIENT_NAME' in df_updatedtech.columns and 'MOBILE_NO' in df_updatedtech.columns:
    # Fetch CRM leads where partner_id is not set and phone is set
    try:
        crm_lead_ids = models.execute_kw(db, uid, password,
            'crm.lead', 'search_read',
            [[['partner_id', '=', False], ['phone', '!=', False]]],  
            {'fields': ['name', 'phone']})
        
        # Clean phone numbers in CRM leads and convert names to string
        for lead in crm_lead_ids:
            lead['phone'] = clean_phone_number(lead['phone'])
            lead['name'] = to_str(lead['name'])
            
    except Exception as e:
        print(f"Error fetching CRM leads: {e}")
        crm_lead_ids = []

    print(f"Number of CRM leads fetched: {len(crm_lead_ids)}")

    # Compare and filter data
    matches = []
    for lead in crm_lead_ids:
        crm_name = to_str(lead['name'])
        crm_phone = to_str(lead['phone'])

        # Check for matches in the Excel data
        matched_rows = df_updatedtech[(df_updatedtech['CLIENT_NAME'] == crm_name) & (df_updatedtech['MOBILE_NO'] == crm_phone)]

        if not matched_rows.empty:
            matches.append({
                'CLIENT_NAME': crm_name,
                'MOBILE_NO': crm_phone
            })

    # Create filtered Excel file if there are matches
    if matches:
        df_matches = pd.DataFrame(matches)
        filtered_excel_file = r"C:\Users\freedom\Desktop\customer\filtered_matches.xlsx"
        try:
            df_matches.to_excel(filtered_excel_file, index=False)
            print(f"Filtered data saved to {filtered_excel_file}")
        except Exception as e:
            print(f"Error saving filtered data to Excel: {e}")
    else:
        print("No matches found or an error occurred during comparison.")
else:
    print("Columns 'CLIENT_NAME' and/or 'MOBILE_NO' not found in the Excel file.")
print("Done")

