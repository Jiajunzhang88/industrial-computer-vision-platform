import sqlite3, json
conn = sqlite3.connect('industrial_ocr.db')
cur = conn.cursor()
cur.execute("UPDATE models SET status='COMPLETED', metrics=?, file_path='models/model_1/weights/best.pt' WHERE id=1",
    (json.dumps({'mAP50': 0.995, 'mAP50-95': 0.86, 'precision': 0.977, 'recall': 1.0, 'epochs': 50}),))
conn.commit()
cur.execute('SELECT id, name, status FROM models WHERE id=1')
print('修复后:', cur.fetchone())
conn.close()
