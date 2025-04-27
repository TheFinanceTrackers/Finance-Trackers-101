import sqlite3
from datetime import datetime, timedelta
import random

# Connect to the SQLite database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# Define the categories, amount ranges, and sample descriptions
categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Healthcare', 'Shopping', 'Others']
amounts = {
    'Housing': (100, 200),
    'Food': (50, 300),
    'Transportation': (30, 150),
    'Entertainment': (50, 400),
    'Healthcare': (40, 250),
    'Shopping': (30, 200),
    'Groceries': (30, 200),
    'Others': (10, 100)
}

# Descriptions for each category
descriptions = {
    'Housing': ['Rent payment', 'Home renovation', 'Utility bills', 'Mortgage payment'],
    'Food': ['Groceries', 'Restaurant bill', 'Takeout', 'Fresh produce purchase'],
    'Transportation': ['Fuel purchase', 'Taxi fare', 'Public transport pass', 'Car maintenance'],
    'Entertainment': ['Movie tickets', 'Concert tickets', 'Theme park visit', 'Game purchase'],
    'Healthcare': ['Doctor consultation', 'Medical prescription', 'Health insurance premium', 'Dental visit'],
    'Shopping': ['Clothing purchase', 'Electronics purchase', 'Gift shopping', 'Online shopping'],
    'Others': ['Miscellaneous expenses', 'Uncategorized spending', 'Unexpected purchase', 'Gift for someone']
}

# Generate the date range from 28/03/2025 to 15/04/2025
start_date = datetime(2025, 3, 28)
end_date = datetime(2025, 4, 15)
date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# Insert 10 entries for each category for each date
for date in date_range:
    for category in categories:
        # Random amount within the specified range for each category
        amount = round(random.uniform(amounts[category][0], amounts[category][1]), 2)
        # Random description for the category
        description = random.choice(descriptions[category])
        # Insert data into the database
        cursor.execute('''
            INSERT INTO "transaction" (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date.strftime('%Y-%m-%d')))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data with descriptions inserted successfully!")
