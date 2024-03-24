import sqlite3
import json

# Load your JSON data
with open('definition.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect('fib_definition.db')
cur = conn.cursor()


# Create tables (assuming they don't already exist)
cur.execute('''CREATE TABLE IF NOT EXISTS Calculations (
               id INTEGER PRIMARY KEY,
               title TEXT,
               description TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Parameters (
               id INTEGER PRIMARY KEY,
               calculation_id INTEGER,
               name TEXT,
               title TEXT,
               description TEXT,
               data_type TEXT,
               data_shape TEXT,
               default_value INT,
               FOREIGN KEY(calculation_id) REFERENCES Calculations(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Outputs (
               id INTEGER PRIMARY KEY,
               calculation_id INTEGER,
               name TEXT,
               title TEXT,
               description TEXT,
               data_type TEXT,
               data_shape TEXT,
               default_value INT,
               FOREIGN KEY(calculation_id) REFERENCES Calculations(id))''')

# Insert data into Calculations table and retrieve the id
cur.execute('INSERT INTO Calculations (title, description) VALUES (?, ?)', (data['title'], data['description']))
calculation_id = cur.lastrowid

# Insert parameters and outputs
for param in data['parameters']:
    cur.execute('INSERT INTO Parameters (calculation_id, name, title, description, data_type, data_shape, default_value) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (calculation_id, param['name'], param['title'], param['description'], param['data_type'], param['data_shape'], param['default_value']))

for output in data['outputs']:
    cur.execute('INSERT INTO Outputs (calculation_id, name, title, description, data_type, data_shape, default_value) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (calculation_id, output['name'], output['title'], output['description'], output['data_type'], output['data_shape'], output['default_value']))

# Commit changes and close connection
conn.commit()
conn.close()
