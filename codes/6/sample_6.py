import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("DELETE FROM recipes WHERE name = '新しい料理';")

# データベースへのコミット
conn.commit()

# SELECT文によるデータの取得
cursor.execute("SELECT name FROM recipes;")

results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()