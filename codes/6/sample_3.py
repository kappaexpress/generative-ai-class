import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("SELECT seasonings, name FROM recipes ORDER BY seasonings DESC")
results = cursor.fetchall()
for row in results:
    print(row)