import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("INSERT INTO recipes (name, abstract, ingredients, steps) VALUES ('新しい料理', '料理の概要', '材料のリスト', '調理手順');")

# データベースへのコミット
conn.commit()

# SELECT文によるデータの取得
cursor.execute("SELECT name FROM recipes;")

results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()