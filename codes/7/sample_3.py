from openai import OpenAI
import streamlit as st
import sqlite3
import json

# Streamlitアプリのタイトルを設定する
st.title("江戸時代の卵料理がわかる君")

# OpenAIクライアントを初期化する
client = OpenAI()

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
    
    # データベースに接続
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    # 仮想テーブルにデータを挿入
    conn.execute(
        "INSERT INTO recipes_fts (name, abstract, ingredients, steps) SELECT name, abstract, ingredients, steps FROM recipes;"
    )

    response_for_query = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {
                "role": "user",
                "content": f"# 質問\n {prompt} \nこの質問でレシピを検索するときに最も重要な単語を教えてください。キーはansを使ってください。",
            },
        ],
    )

    print(response_for_query.choices[0].message.content)

    # response_for_query.choices[0].message.contentはJSON形式の文字列で、キーがansの値を取得する
    query = json.loads(response_for_query.choices[0].message.content)["ans"]

    # 仮想テーブルのデータを全文検索
    cursor.execute(f"SELECT * FROM recipes_fts WHERE steps MATCH '{query}';")

    results = cursor.fetchall()

    print(results)

    # データベースのクローズ
    conn.close()

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
