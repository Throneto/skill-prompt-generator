
import sqlite3

conn = sqlite3.connect('extracted_results/elements.db')
cursor = conn.cursor()

# Fix "black hair hair"
cursor.execute("UPDATE elements SET ai_prompt_template = 'black hair' WHERE name = 'black_hair' AND ai_prompt_template = 'black hair hair'")
print(f"Fixed black_hair: {cursor.rowcount} rows updated")

conn.commit()
conn.close()
