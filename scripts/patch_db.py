

import sqlite3
import sys
import os

sys.path.append(os.getcwd())
from skill_library.constants import DEFAULT_DB_PATH

conn = sqlite3.connect(DEFAULT_DB_PATH)
cursor = conn.cursor()

# Fix "black hair hair"
cursor.execute("UPDATE elements SET ai_prompt_template = 'black hair' WHERE name = 'black_hair' AND ai_prompt_template = 'black hair hair'")
print(f"Fixed black_hair: {cursor.rowcount} rows updated")

conn.commit()
conn.close()
