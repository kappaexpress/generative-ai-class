import sqlite_vss
from openai import OpenAI
import streamlit as st
import sqlite3
import numpy as np
from typing import List

# OpenAIクライアントを初期化する
client = OpenAI()


# 埋め込みベクトルをシリアライズする関数
def serialize(vector: List[float]) -> bytes:
    return np.asarray(vector).astype(np.float32).tobytes()


# テキストから埋め込みベクトルを生成する関数
def generate_embedding(text: str) -> List[float]:
    response = client.embeddings.create(model="text-embedding-3-large", input=[text])
    return response.data[0].embedding

# Streamlitアプリのタイトルを設定する
st.title("江戸時代の卵料理がわかる君")


# セッション状態にモデルが設定されていない場合に初期化する
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# セッション状態にメッセージリストが存在しない場合に初期化する
if "messages" not in st.session_state:
    st.session_state.messages = []

# これまでのメッセージをチャットインターフェースに表示する
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーが新しいメッセージを入力できるテキストボックス
if prompt := st.chat_input("質問やメッセージを入力してください"):
    # 新しいユーザーメッセージをセッション状態に追加する
    st.session_state.messages.append({"role": "user", "content": prompt})
    # チャットインターフェースにユーザーメッセージを表示する
    with st.chat_message("user"):
        st.markdown(prompt)
    
    query_embedding = generate_embedding(prompt)
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
    results = con.execute(query, (serialized_embedding, 3)).fetchall()
    con.close()

    print(results)

    # データベースのクローズ
    con.close()

    # チャットメッセージをOpenAI APIに送信するために整形する
    message = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    # messageの先頭にシステムメッセージを追加する
    message.insert(
        0,
        {
            "role": "system",
            "content": f"# レシピ検索結果\n {results} \nこれはレシピ検索結果です。これに基づいて質問に答えます。レシピ検索結果がない場合は、「データにありません」を出力します。",
        },
    )

    # これまでのチャットメッセージをOpenAI APIに送信し、アシスタントの応答を表示する
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=message,
            stream=True,
        )
        # OpenAIからの応答を取得し、チャットインターフェースに表示する
        response = st.write_stream(stream)
    # アシスタントの応答をセッション状態に追加する
    st.session_state.messages.append({"role": "assistant", "content": response})
