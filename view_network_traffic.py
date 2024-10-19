import sqlite3

conn = sqlite3.connect('network_usage.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM daily_usage')
rows = cursor.fetchall()
for row in rows:
    print(f"Date: {row[0]}, Download: {row[1]} MB, Upload: {row[2]} MB")
conn.close()
