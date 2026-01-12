
import sqlite3
import json

conn = sqlite3.connect('extracted_results/elements.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM elements WHERE name = 'black_hair'")
row = cursor.fetchone()
print("black_hair element:", row)

cursor.execute("SELECT * FROM elements WHERE name = 'layouts' OR category = 'layouts' LIMIT 1")
print("layouts sample:", cursor.fetchone())

conn.close()
