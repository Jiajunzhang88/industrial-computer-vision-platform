import sqlite3
c = sqlite3.connect('industrial_ocr.db')
cols = [r[1] for r in c.execute('PRAGMA table_info(cv_operations)')]
print('cols before:', cols)
if 'output_type' not in cols:
    c.execute("ALTER TABLE cv_operations ADD COLUMN output_type VARCHAR(20) NOT NULL DEFAULT 'image'")
    c.commit()
    print('column added')
else:
    print('column already exists')
print('cols after:', [r[1] for r in c.execute('PRAGMA table_info(cv_operations)')])
