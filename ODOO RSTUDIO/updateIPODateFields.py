import xmlrpc.client
from datetime import datetime

# Odoo connection parameters
url = 'https://crmindira-crm-22octstaging-16000205.dev.odoo.com/'
db = 'crmindira-crm-22octstaging-16000205'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Initialize the connection to Odoo
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Function to convert date format to 'September 10, 2024'
def convert_date_format(date_str):
    # List of possible date formats in the data
    formats = ["%d-%b-%y", "%b-%d-%Y", "%b %d, %Y", "%d-%B-%y", "%B-%d-%Y"]
    for fmt in formats:
        try:
            # Attempt to parse the date string using each format
            date_obj = datetime.strptime(date_str, fmt)
            # Return the date in the desired format if successful
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            continue  # Try the next format if parsing fails
    print(f"Invalid date format: {date_str}")
    return None

# Function to check if the date is in the required format (e.g., 'September 10, 2024')
def is_valid_format(date_str):
    try:
        # Try to parse the date in the expected format
        datetime.strptime(date_str, "%B %d, %Y")  # Expected format
        return True
    except ValueError:
        return False

# Fetch all records from the x_ipo model
x_ipo_records = models.execute_kw(
    db, uid, password,
    'x_ipo', 'search_read',
    [],  # No domain filter, fetch all records
    {'fields': ['id', 'x_open_date', 'x_close_date', 'x_listing_date']}  # Fetch the date fields
)

# Loop through each record and check if the dates are in the correct format
for record in x_ipo_records:
    record_id = record['id']
    x_open_date = record.get('x_open_date')
    x_close_date = record.get('x_close_date')
    x_listing_date = record.get('x_listing_date')

    update_values = {}

    # Check and update x_open_date if needed
    if x_open_date and not is_valid_format(x_open_date):
        new_open_date = convert_date_format(x_open_date)
        if new_open_date:
            update_values['x_open_date'] = new_open_date
            print(f"Record {record_id}: x_open_date updated to {new_open_date}")
    
    # Check and update x_close_date if needed
    if x_close_date and not is_valid_format(x_close_date):
        new_close_date = convert_date_format(x_close_date)
        if new_close_date:
            update_values['x_close_date'] = new_close_date
            print(f"Record {record_id}: x_close_date updated to {new_close_date}")

    # Check and update x_listing_date if needed
    if x_listing_date and not is_valid_format(x_listing_date):
        new_listing_date = convert_date_format(x_listing_date)
        if new_listing_date:
            update_values['x_listing_date'] = new_listing_date
            print(f"Record {record_id}: x_listing_date updated to {new_listing_date}")
    
    # If any updates were made, write the changes to the record
    if update_values:
        models.execute_kw(
            db, uid, password,
            'x_ipo', 'write',
            [[record_id], update_values]
        )
        print(f"Record {record_id} updated with values: {update_values}")

print("Done")
