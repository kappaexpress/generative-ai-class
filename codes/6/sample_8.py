import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 仮想テーブルにデータを挿入
conn.execute("INSERT INTO recipes_fts (name, abstract, ingredients, steps) SELECT name, abstract, ingredients, steps FROM recipes;")

# 仮想テーブルのデータを全文検索
cursor.execute("SELECT name, steps FROM recipes_fts WHERE steps MATCH 'レンジ';")

results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()