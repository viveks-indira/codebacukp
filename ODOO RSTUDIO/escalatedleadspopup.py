import xmlrpc.client
import pandas as pd
from datetime import datetime, timedelta, date

class CRMActivityManager:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    def get_inactive_clients(self):
        next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        domain = [('x_studio_current_week', '=', 0), ('x_studio_current_month', '>', 0)]
        lead_ids = self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'search', [domain])
        fields_to_read = ['id', 'user_id', 'x_studio_next_reminder_date']

        inactive_clients = self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'read', [lead_ids, fields_to_read])
        for client in inactive_clients:
            if isinstance(client['user_id'], list):
                client['user_id'] = client['user_id'][0]

        df_inactive_clients = pd.DataFrame(inactive_clients).sort_values(by='user_id')
        
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        domain = ['|',['activity_ids.date_deadline', '<', today.strftime('%Y-%m-%d')],['activity_ids.date_deadline', '=', tomorrow.strftime('%Y-%m-%d')]]
        ext_lead_ids = self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'search', [domain])
        df_ext_lead_ids = pd.DataFrame(ext_lead_ids, columns=['id'])
        df_inactive_clients = df_inactive_clients[~df_inactive_clients['id'].isin(df_ext_lead_ids['id'])]
    
        df_inactive_clients['x_studio_next_reminder_date'] = df_inactive_clients['x_studio_next_reminder_date'].astype(str)
        df_inactive_clients = df_inactive_clients[(df_inactive_clients['x_studio_next_reminder_date'] <= today.strftime('%Y-%m-%d'))|(df_inactive_clients['x_studio_next_reminder_date'] == 'False')]

        return df_inactive_clients

    def get_existing_activities(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        domain = ['|',['activity_ids.date_deadline', '<', today.strftime('%Y-%m-%d')],['activity_ids.date_deadline', '=', tomorrow.strftime('%Y-%m-%d')]]
        fields = ['user_id']
        group_by = ['user_id']
        activities = self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'read_group', [domain, fields, group_by], {'lazy': False})

        data = [{'Salesperson ID': activity['user_id'][0], 'Activity Count': activity['__count']} for activity in activities]
        df_existing_activities = pd.DataFrame(data).sort_values(by='Salesperson ID')
        print(f"Retrieved {len(df_existing_activities)} existing activities.")
        return df_existing_activities

    def merge_dataframes(self, df_inactive_clients, df_existing_activities):
        df_merged = df_inactive_clients.merge(df_existing_activities, left_on='user_id', right_on='Salesperson ID', how='outer')
        df_merged['user_id'] = df_merged['user_id'].combine_first(df_merged['Salesperson ID'])
        df_merged = df_merged.fillna(0).astype({
            'user_id': 'int',
            'Salesperson ID': 'int',
            'id': 'int',
            'Activity Count': 'int'
        })

        df_merged = df_merged.drop(df_merged[df_merged['id'] == 0].index)

        df_merged = df_merged[(df_merged['Activity Count'] < 10) | (df_merged['Activity Count'] == 0)]
        print(f"Merged data contains {len(df_merged)} entries eligible for follow-up activities.")
        return df_merged

    def create_follow_up_activities(self, df_merged):
        next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        activity_type_name = 'Call'
        activity_type_id = self.models.execute_kw(self.db, self.uid, self.password, 'mail.activity.type', 'search', [[('name', '=', activity_type_name)]], {'limit': 1})
        activity_type_id = activity_type_id[0] if activity_type_id else False

        activity_counts = {}
        activities_to_create = []

        for index, row in df_merged.iterrows():
            salesperson_id = row['user_id']
            lead_id = row['id']

            if salesperson_id not in activity_counts:
                activity_counts[salesperson_id] = row['Activity Count']

            current_activity_count = activity_counts[salesperson_id]

            if current_activity_count < 10 and lead_id != 0:
                activity_vals = {
                    'res_model_id': int(self.models.execute_kw(self.db, self.uid, self.password, 'ir.model', 'search', [[('model', '=', 'crm.lead')]], {'limit': 1})[0]),
                    'res_id': int(lead_id),
                    'activity_type_id': int(activity_type_id),
                    'summary': 'Call Follow-up Activity',
                    'note': 'Please make a follow-up call to the client.',
                    'date_deadline': next_day,
                    'user_id': int(salesperson_id),
                }

                # existing_activity_check = self.models.execute_kw(
                #     self.db, self.uid, self.password,
                #     'crm.lead', 'search_count',
                #     [[('id', '=', int(lead_id)), ('activity_state', 'in', ['today', 'overdue'])]]
                # )
                  
                activities_to_create.append(activity_vals)
                activity_counts[salesperson_id] += 1
                  
                # if existing_activity_check == 0:
                #     
                # else:
                #     print(f"Activity already exists for lead ID {lead_id}.")
            else:
                print(f"Skipping lead ID {lead_id}; either existing activities or invalid ID.")

        if activities_to_create:
            new_activity_ids = self.models.execute_kw(self.db, self.uid, self.password, 'mail.activity', 'create', [activities_to_create])
            print(f"Activities created with IDs: {new_activity_ids}")
        else:
            print("No activities to create.")

    # def escalate_leads(self):
    #     today = datetime.now()
    #     two_days_ago = today - timedelta(days=2)
    #     date_deadline = two_days_ago.strftime('%Y-%m-%d')
    # 
    #     escalated_leads = self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'search_read', [[['activity_ids.date_deadline', '<=', date_deadline]]], {'fields': ['id', 'name', 'activity_ids', 'x_studio_escalated_lead']})
    # 
    #     for lead in escalated_leads:
    #         lead_id = lead['id']
    #         self.models.execute_kw(self.db, self.uid, self.password, 'crm.lead', 'write', [[lead_id], {'x_studio_escalated_lead': 1}])
    #     
    #     print(f"Escalated {len(escalated_leads)} leads.")
        

        
manager = CRMActivityManager(url='https://crmindira-crm-19julystaging-14299297.dev.odoo.com/', 
db='crmindira-crm-19julystaging-14299297',
username='sharshit@indiratrade.com', password='Crm@123')
df_inactive_clients = manager.get_inactive_clients()
df_existing_activities = manager.get_existing_activities()
df_merged = manager.merge_dataframes(df_inactive_clients, df_existing_activities)
manager.create_follow_up_activities(df_merged)
#manager.escalate_leads()
print("done")

