import sqlite3
conn = sqlite3.connect('industrial_ocr.db')
cursor = conn.cursor()
cursor.execute('SELECT id, name, status FROM models')
rows = cursor.fetchall()
for row in rows:
    print(f'ID: {row[0]}, Name: {row[1]}, Status: {row[2]}')
conn.close()
