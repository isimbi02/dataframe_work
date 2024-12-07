import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder

try:
    trainer_api = requests.get('http://127.0.0.1:8000/members/all-trainers/')
    trainer_api.raise_for_status()
    trainer_api_data = trainer_api.json()
    members_api = requests.get('http://127.0.0.1:8000/members/all-members/')
    members_api.raise_for_status()
    members_api_data = members_api.json()

    schedules_api = requests.get('http://127.0.0.1:8000/schedules/all-schedules/')
    schedules_api_data = schedules_api.json()
    
    mdf = pd.DataFrame(members_api_data['users'])
    tdf = pd.DataFrame(trainer_api_data['trainers'])
    sdf = pd.DataFrame(schedules_api_data["schedules"])

    mdf = mdf.rename(columns={'id': 'member_id', 'name': 'member_name', 'email': 'member_email'})
    tdf = tdf.rename(columns={'id': 'trainer_id', 'name': 'trainer_name', 'expertise': 'trainer_expertise'})
    sdf = sdf.rename(columns={'member': 'member_id', 'trainer': 'trainer_id', 'session_date': 'session_date', 'session_time': 'session_time'})

    merged_df = pd.merge(sdf, mdf, on='member_id', how='inner')
    merged_df = pd.merge(merged_df, tdf, on='trainer_id', how='inner')

    merged_df['session_date'].fillna('2024-12-10', inplace=True) 

    merged_df['month'] = pd.to_datetime(merged_df['session_date']).dt.month
    

    label_encoder = LabelEncoder()
    merged_df['trainer_expertise_encoded'] = label_encoder.fit_transform(merged_df['trainer_expertise'])

    print(merged_df.describe())
    print(merged_df.shape)
    print(merged_df.head())
except requests.exceptions.RequestException as e:
    print(f"error fetching data from API: {e}")
