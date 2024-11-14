import xmlrpc.client
import pandas as pd

url = 'https://crmindira-crm-22octstaging-16000205.dev.odoo.com/'
db = 'crmindira-crm-22octstaging-16000205'
username = 'sharshit@indiratrade.com'
password = 'Crm@123'

# Set up the XML-RPC connection
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# # Load the DataFrame (replace with your actual DataFrame)
# df = pd.DataFrame({
#     'Issuer Company': ['Company1', 'Company2', 'Company3'],
#     'Open Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
#     'Close Date': ['2024-01-05', '2024-01-06', '2024-01-07'],
#     'Listing Date': ['2024-01-10', '2024-01-12', '2024-01-14'],
#     'Issue Price': [100, 200, 150],
#     'Issue Size': [1000000, 2000000, 1500000],
#     'Lot Size': [10, 20, 15],
#     'Conclusion Rationale with business overview': ['Overview1', 'Overview2', 'Overview3'],
#     'Business Brief': ['Brief1', 'Brief2', 'Brief3'],
#     'Retail Lot': [500, 600, 550],
#     'SHNI': [100, 200, 150],
#     'BHNI': [50, 100, 75],
#     'Posting Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
#     'Preksha Status': ['Status1', 'Status2', 'Status3']
# })

data = pd.read_excel(r"C:\Users\freedom\Downloads\New Microsoft Excel Worksheet.xlsx")
df = pd.DataFrame(data)

df[['Open Date', 'Close Date', 'Listing Date', 'Posting Date']] = df[['Open Date', 'Close Date', 'Listing Date', 'Posting Date']].astype(str)


# Stack to hold the top 20 "Issuer Company" records
issuer_stack = []

# Push "Issuer Company" of top 20 records to stack
for index, row in df.head(20).iterrows():
    issuer_stack.append(row['Issuer Company'])

# Iterate through stack elements and perform matching with Odoo model
while issuer_stack:
    issuer_company = issuer_stack.pop()
    
    # Search for existing records in x_ipo model by matching "Issuer Company" with x_company
    ipo_record = models.execute_kw(db, uid, password,
                                   'x_ipo', 'search',
                                   [[('x_company', '=', issuer_company)]],
                                   {'limit': 1})
    ipo_record_df=pd.DataFrame(ipo_record)
    
    # If record found, update it; otherwise, create a new record
    if ipo_record:
        ipo_id = ipo_record[0]
        # Prepare values to update
        for index, row in df.iterrows():
            if row['Issuer Company'] == issuer_company:
                 # Set value for x_studio_reccomendation based on Conclusion
                if row['Conclusion'] == 'Apply':
                    recommendation = '3'  # 3 stars for 'Apply'
                elif row['Conclusion'] == 'Neutral':
                    recommendation = '2'  # 2 stars for 'Neutral'
                elif row['Conclusion'] == 'Ignore':
                    recommendation = '0'  # No stars for 'Ignore'
                values = {
                    'x_company': row['Issuer Company'],
                    'x_open_date': row['Open Date'],
                    'x_close_date': row['Close Date'],
                    'x_listing_date': row['Listing Date'],
                    'x_issue_price': row['Issue Price (Rs)'],
                    'x_issue_size': row['Issue Size (Rs Cr.)'],
                    'x_lot_size': row['Lot Size'],
                    'x_studio_conclusion_rationale_with_business_overview': row['Conclusion Rationale with business overview'],
                    'x_studio_business_brief': row['Business Brief'],
                    'x_studio_retail_lot': row['Retail Lot'],
                    'x_studio_shni': row['SHNI'],
                    'x_studio_bhni': row['BHNI'],
                    'x_studio_posting_date': row['Posting Date'],
                    'x_studio_peer_status': row['Preksha Status'],
                    'x_studio_reccomendation': recommendation,  # Update recommendation
                }
                # Update the record in Odoo
                models.execute_kw(db, uid, password,
                                  'x_ipo', 'write',
                                  [[ipo_id], values])
                print(f"Updated record for company: {issuer_company}")
                break
    else:
        # Prepare values to create a new record
        for index, row in df.iterrows():
            if row['Issuer Company'] == issuer_company:
                 # Set value for x_studio_reccomendation based on Conclusion
                if row['Conclusion'] == 'Apply':
                    recommendation = '3'  # 3 stars for 'Apply'
                elif row['Conclusion'] == 'Neutral':
                    recommendation = '2'  # 2 stars for 'Neutral'
                elif row['Conclusion'] == 'Ignore':
                    recommendation = '0'  # No stars for 'Ignore'
                values = {
                    'x_exchange': row['Exchange'],
                    'x_company': row['Issuer Company'],
                    'x_open_date': row['Open Date'],
                    'x_close_date': row['Close Date'],
                    'x_listing_date': row['Listing Date'],
                    'x_issue_price': row['Issue Price (Rs)'],
                    'x_issue_size': row['Issue Size (Rs Cr.)'],
                    'x_lot_size': row['Lot Size'],
                    'x_studio_conclusion_rationale_with_business_overview': row['Conclusion Rationale with business overview'],
                    'x_studio_business_brief': row['Business Brief'],
                    'x_studio_retail_lot': row['Retail Lot'],
                    'x_studio_shni': row['SHNI'],
                    'x_studio_bhni': row['BHNI'],
                    'x_studio_posting_date': row['Posting Date'],
                    'x_studio_peer_status': row['Preksha Status'],
                    'x_studio_reccomendation': recommendation,  # Update recommendation
                }
                # Create a new record in Odoo
                models.execute_kw(db, uid, password,
                                  'x_ipo', 'create',
                                  [values])
                print(f"Created record for company: {issuer_company}")
                break

print("All ipo updated and created")
