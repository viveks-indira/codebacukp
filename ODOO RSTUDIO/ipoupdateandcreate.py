import csv
import xmlrpc.client
from datetime import datetime

# Odoo connection details
# Connect to Odoo
url = 'https://crmindira-crm-22octstaging-16000205.dev.odoo.com//'
db = 'crmindira-crm-22octstaging-16000205'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'


# Initialize the connection
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

csv_file_path = r"C:\Users\freedom\Downloads\IPO - Main Board - Odoo - IPO - Facts Summary.csv"

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Clean up 'Issue Price' and 'Issue Size' by removing commas
        issue_price = row['Issue Price (Rs)'].replace(',', '')  # Remove commas
        issue_size = row['Issue Size (Rs Cr.)'].replace(',', '')  # Remove commas

        # Create a dictionary with field names and values to create or update
        record_data = {
            'x_company': row['Issuer Company'],
            'x_issue_price': float(issue_price) if issue_price else 0.0,
            'x_issue_size': float(issue_size) if issue_size else 0.0,
            'x_open_date': row['Open Date'],
            'x_close_date': row['Close Date'],
            'x_listing_date': row['Listing Date'],
            'x_exchange': row['Exchange'],
            'x_studio_conclusion_rationale_with_business_overview': row['Conclusion Rationale with business overview'],
            'x_studio_business_brief': row['Business Brief'],
        }

        # Check if the record already exists in Odoo
        existing_record = models.execute_kw(db, uid, password, 'x_ipo', 'search_read', [[('x_company', '=', row['Issuer Company'])]], {'fields': ['id']})

        if existing_record:
            # Update existing record
            models.execute_kw(db, uid, password, 'x_ipo', 'write', [[existing_record[0]['id']], record_data])
            print(f"Updated record for company: {row['Issuer Company']}")
        else:
            # Create a new record
            models.execute_kw(db, uid, password, 'x_ipo', 'create', [record_data])
            print(f"Created new record for company: {row['Issuer Company']}")

print("done")
