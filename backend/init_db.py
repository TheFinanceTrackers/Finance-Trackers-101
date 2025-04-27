import sqlite3

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# You can also create the transactions table here if not already created

conn.commit()
conn.close()
