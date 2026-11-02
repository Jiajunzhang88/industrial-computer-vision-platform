import sqlite3, datetime
conn = sqlite3.connect("industrial_ocr.db")
cur = conn.cursor()
now = datetime.datetime.now().isoformat()
cur.execute("UPDATE models SET status='FAILED', metrics=?, updated_at=? WHERE id=3",
            ('{"note":"training stopped by user"}', now))
conn.commit()
cur.execute("SELECT id,name,status,metrics FROM models")
for r in cur.fetchall():
    print(r)
conn.close()
