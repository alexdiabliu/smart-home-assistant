
import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("alarms.db")

# Create a cursor object
cursor = conn.cursor()

# Create the alarms table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT NOT NULL,
        label TEXT,
        triggered INTEGER DEFAULT 0
    )
''')

# Commit and close
conn.commit()
conn.close()
