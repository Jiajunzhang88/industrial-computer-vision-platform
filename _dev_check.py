import sqlite3
conn = sqlite3.connect("industrial_ocr.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(devices)")
cols = [r[1] for r in cur.fetchall()]
print("cols:", cols)
cur.execute("SELECT * FROM devices")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
