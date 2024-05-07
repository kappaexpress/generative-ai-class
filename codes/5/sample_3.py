import streamlit as st
import pandas as pd
import numpy as np

# サイドバーの追加
sidebar = st.sidebar
sidebar.title("サイドバー")
sidebar.write("ここはサイドバーです。任意のウィジェットを追加できます。")

# サイドバーにセレクタを追加
options = ["オプション1", "オプション2", "オプション3"]
choice = sidebar.selectbox("選択してください:", options)
sidebar.write(f"選択されたオプション: {choice}")

# メインページのカラムレイアウト
col1, col2 = st.columns(2)
with col1:
    st.header("カラム1")
    st.write("ここはカラム1です。任意のコンテンツを表示できます。")

    # 地図の表示
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [38.26822, 140.86942], columns=["lat", "lon"]
    )
    st.map(map_data)

with col2:
    st.header("カラム2")
    st.write("ここはカラム2です。さらに異なるコンテンツを表示できます。")

    # グラフの表示
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)


st.header("プレースホルダを使用したメッセージの一時的な表示と要素の非表示")
# プレースホルダを使用したメッセージの一時的な表示と要素の非表示

# 要素の非表示
placeholder = st.empty()

if st.button('非表示にする'):
    placeholder.empty()
else:
    placeholder.write('ボタンを押すとこのメッセージが非表示になります。')