import sqlite3


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(f'SELECT * FROM card;')
print(cur.fetchall())
