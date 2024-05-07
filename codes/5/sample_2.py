import streamlit as st

st.title("ユーザー入力の取得")

# テキスト入力
name = st.text_input("お名前を入力してください", "")
st.write(f"あなたの名前は {name} です")

# 数値入力
age = st.number_input("年齢を入力してください", min_value=0, max_value=150, step=1)
st.write(f"あなたの年齢は {age} 歳です")

# 選択肢（セレクトボックス）
color = st.selectbox("好きな色を選んでください", ("赤", "青", "緑", "黄"))
st.write(f"あなたの好きな色は {color} です")

# 選択肢（ラジオボタン）
gender = st.radio("性別を選択してください", ("男性", "女性"))
st.write(f"あなたの性別は {gender} です")

# 選択肢（マルチセレクト）
fruits = st.multiselect("好きな果物を選んでください（複数選択可）", ("りんご", "バナナ", "オレンジ", "ぶどう"))
st.write(f"あなたの好きな果物は {', '.join(fruits)} です")

# ファイルのアップロード
uploaded_file = st.file_uploader("ファイルをアップロードしてください")
if uploaded_file is not None:
    file_content = uploaded_file.read()
    st.write(f"アップロードされたファイルの内容:\n{file_content}")