import sqlite3, datetime
conn = sqlite3.connect("industrial_ocr.db")
cur = conn.cursor()
now = datetime.datetime.now().isoformat()
cur.execute("UPDATE models SET status='FAILED', metrics=?, updated_at=? WHERE id=3",
            ('{"note":"training interrupted by server restart"}', now))
conn.commit()
cur.execute("SELECT id,status FROM models")
for r in cur.fetchall():
    print(r)
conn.close()
