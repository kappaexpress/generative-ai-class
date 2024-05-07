import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("UPDATE recipes SET abstract = 'パーティー向け' WHERE name = '新しい料理';")

# データベースへのコミット
conn.commit()

# SELECT文によるデータの取得
cursor.execute("SELECT name, abstract FROM recipes;")

results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()