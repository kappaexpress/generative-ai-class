import sqlite3

# データベースに接続
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SELECT文によるデータの取得
cursor.execute("SELECT name, food_category_1, ingredients FROM recipes WHERE food_category_1 = '野菜';")
results = cursor.fetchall()
for row in results:
    print(row)

# データベースのクローズ
conn.close()