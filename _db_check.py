import sqlite3
conn = sqlite3.connect("industrial_ocr.db")
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("tables:", [r[0] for r in cur.fetchall()])
cur.execute("PRAGMA table_info(models)")
print("cols:", [r[1] for r in cur.fetchall()])
cur.execute("SELECT id,name,status,file_path,dataset_id FROM models")
for r in cur.fetchall():
    print(r)
