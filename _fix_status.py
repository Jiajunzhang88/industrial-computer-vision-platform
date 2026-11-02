import sqlite3
conn = sqlite3.connect('industrial_ocr.db')
cur = conn.cursor()
# 修正状态为大写枚举
cur.execute("UPDATE models SET status='NOT_STARTED' WHERE id=1")
conn.commit()
cur.execute('SELECT id, status FROM models WHERE id=1')
print('修正后:', cur.fetchone())
conn.close()
