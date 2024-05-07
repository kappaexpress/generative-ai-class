import streamlit as st
import pandas as pd
import numpy as np

# アプリケーションのタイトルを設定
st.title("Streamlitアプリケーションのサンプル")

# テキストの表示
st.header("テキストの表示")
st.write("これはst.writeを使用したテキストです。")
st.subheader("サブヘッダーのテキスト")

# データの表示
st.header("データの表示")
df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
st.write("データフレーム:")
st.dataframe(df)
st.write("テーブル:")
st.table(df)

# グラフの表示
st.header("グラフの表示")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)

chart_data = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])
st.bar_chart(chart_data)

# 地図の表示
st.header("地図の表示")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [38.26822, 140.86942], columns=["lat", "lon"]
)
st.map(map_data)
