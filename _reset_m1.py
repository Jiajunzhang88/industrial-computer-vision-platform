import sqlite3
conn = sqlite3.connect('industrial_ocr.db')
cur = conn.cursor()
cur.execute("UPDATE models SET status='NOT_STARTED', metrics=NULL, file_path=NULL WHERE id=1")
conn.commit()
print('模型1已重置为 NOT_STARTED')
conn.close()
