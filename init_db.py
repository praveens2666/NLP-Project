import sqlite3

# Create database connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create table with correct column names
cursor.execute('''
CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT NOT NULL,
    tokenized_output TEXT NOT NULL,
    expert_correction TEXT
)
''')

# Save and close
conn.commit()
conn.close()

print("Database initialized successfully!")
