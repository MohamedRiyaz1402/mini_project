import sqlite3

# Initialize database connection for configuration
config_conn = sqlite3.connect('config.db')
config_c = config_conn.cursor()

# Create a table to store configurations (if not already created)
config_c.execute('''
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        threshold INTEGER,
        interval INTEGER
    )
''')
config_conn.commit()

# Update default values in the config table
config_c.execute("INSERT INTO config (threshold, interval) VALUES (?, ?)", (91, 10))

config_conn.commit()
config_conn.close()

conn = sqlite3.connect('alarms.db')
c = conn.cursor()

# Create a table to store alarms (if not already created)
c.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        action TEXT
    )
''')
conn.commit()
conn.close()
