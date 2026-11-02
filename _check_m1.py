import sqlite3
conn = sqlite3.connect('industrial_ocr.db')
cur = conn.cursor()
cur.execute('SELECT id, name, status, metrics, file_path FROM models WHERE id=1')
row = cur.fetchone()
print(f"id={row[0]} name={row[1]} status={row[2]}")
print(f"metrics={row[3]}")
print(f"file_path={row[4]}")
# 改回 COMPLETED
cur.execute("UPDATE models SET status='COMPLETED' WHERE id=1")
conn.commit()
print('已改回 COMPLETED')
conn.close()
