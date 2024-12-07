import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Database connection
conn = psycopg2.connect(
    dbname="fitnessclubmanagement",
    user="postgres",
    password="123456",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Fetch all Member and Trainer IDs from the database
cursor.execute("SELECT id FROM members_member")
member_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM trainers_trainer")
trainer_ids = [row[0] for row in cursor.fetchall()]

# Function to generate random session date and time
def generate_random_datetime():
    # Generate a random date in the past 2 years
    random_date = fake.date_between(start_date='-2y', end_date='today')
    # Generate a random time between 6 AM and 8 PM
    random_time = fake.time_object(end_datetime=None)
    return random_date, random_time

# Function to generate dummy schedule data
def generate_dummy_schedules(num_schedules):
    schedules_data = []
    
    for _ in range(num_schedules):
        # Randomly select a member and a trainer
        member_id = random.choice(member_ids)
        trainer_id = random.choice(trainer_ids)
        
        # Generate random session date and time
        session_date, session_time = generate_random_datetime()
        
        # Prepare data for bulk insert
        schedules_data.append((member_id, trainer_id, session_date, session_time))
    
    # Insert schedules into the database in bulk
    cursor.executemany(
        """
        INSERT INTO schedules_schedule (member_id, trainer_id, session_date, session_time)
        VALUES (%s, %s, %s, %s)
        """,
        schedules_data
    )
    
    print(f"Successfully inserted {num_schedules} schedules.")

# Generate 500,000 dummy schedules
generate_dummy_schedules(500000)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data has been successfully processed and saved to the 'schedules_schedule' table.")


