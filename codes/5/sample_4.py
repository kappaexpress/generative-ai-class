from openai import OpenAI
import streamlit as st

# Streamlitアプリのタイトルを設定する
st.title("ChatGPTみたいなものを作ってみる")

# OpenAIクライアントを初期化する
client = OpenAI()

# セッション状態にモデルが設定されていない場合に初期化する
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-2024-04-09"

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

    # チャットメッセージをOpenAI APIに送信するために整形する
    message = [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    # messageの先頭にシステムメッセージを追加する
    message.insert(
        0,
        {
            "role": "system",
            "content": "あなたはうさぎです。語尾にぴょんを付けてください。",
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
