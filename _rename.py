import sqlite3
c = sqlite3.connect('industrial_ocr.db')
cur = c.cursor()
cur.execute("UPDATE models SET name='test_coin' WHERE id=1")
c.commit()
cur.execute('SELECT id, name FROM models WHERE id=1')
print('已改为:', cur.fetchone())
c.close()
