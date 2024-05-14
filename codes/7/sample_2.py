import sqlite3
import numpy as np
import openai
from typing import List
import sqlite_vss


# ベクトル検索を行う関数
def search_similar_steps(query_text: str, k: int = 3):
    query_embedding = generate_embedding(query_text)
    serialized_embedding = serialize(query_embedding)

    con = sqlite3.connect("example_vec.db")
    con.enable_load_extension(True)
    sqlite_vss.load(conn=con)

    query = """
    SELECT recipes.*, recipes_vec.distance
    FROM recipes_vec
    JOIN recipes ON recipes_vec.rowid = recipes.rowid
    WHERE vss_search(recipes_vec.steps_vec, vss_search_params(?, 10))
    ORDER BY recipes_vec.distance
    LIMIT ?;
    """
    results = con.execute(query, (serialized_embedding, k)).fetchall()
    con.close()
    return results


# 埋め込みベクトルをシリアライズする関数
def serialize(vector: List[float]) -> bytes:
    return np.asarray(vector).astype(np.float32).tobytes()


# テキストから埋め込みベクトルを生成する関数
def generate_embedding(text: str) -> List[float]:
    response = openai.embeddings.create(model="text-embedding-3-large", input=[text])
    return response.data[0].embedding


# ベクトル検索を実行する
query_text = "日本酒"
results = search_similar_steps(query_text)

for result in results:
    print(f"Name: {result[6]}")
    print(f"Abstract: {result[7]}")
    print(f"Ingredients: {result[8]}")
    print(f"Steps: {result[9]}")
    print(f"Distance: {result[10]}\n")
