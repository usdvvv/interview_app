import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# Create responses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response TEXT,
    sentiment TEXT,
    confidence REAL,
    relevance TEXT,
    relevance_score REAL,
    category TEXT
)
""")

conn.commit()
conn.close()
print("Database created successfully.")
