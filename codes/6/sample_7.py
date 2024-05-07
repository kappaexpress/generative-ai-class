import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("SELECT recipes.name, like FROM recipes JOIN (SELECT * FROM like WHERE like = True) AS like ON recipes.name = like.name;")

results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()