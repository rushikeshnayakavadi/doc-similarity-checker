import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("src/database.db")  # Ensure path is correct
cursor = conn.cursor()

# Create a table to store documents
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

# Commit and close the connection
conn.commit()
conn.close()

print("✅ Database and table created successfully!")
