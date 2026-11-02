import sqlite3, datetime
conn = sqlite3.connect("industrial_ocr.db")
cur = conn.cursor()
now = datetime.datetime.utcnow().isoformat()
# 模型2 实际已完成训练(best.pt有效,已修类别名), 修正状态与指标
cur.execute("UPDATE models SET status='COMPLETED', metrics=?, updated_at=? WHERE id=2",
            (('{"mAP50":0.706,"P":0.627,"R":0.698,"epochs":30,"elapsed_sec":383.4}'), now))
cur.execute("SELECT id,status,file_path FROM models")
for r in cur.fetchall():
    print(r)
conn.commit()
conn.close()
