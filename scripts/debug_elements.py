

import sqlite3
import json
import sys
import os

sys.path.append(os.getcwd())
from skill_library.constants import DEFAULT_DB_PATH

conn = sqlite3.connect(DEFAULT_DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM elements WHERE name = 'black_hair'")
row = cursor.fetchone()
print("black_hair element:", row)

cursor.execute("SELECT * FROM elements WHERE name = 'layouts' OR category = 'layouts' LIMIT 1")
print("layouts sample:", cursor.fetchone())

conn.close()
