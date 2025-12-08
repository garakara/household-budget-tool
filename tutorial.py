import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Streamlit チュートリアル")

# 1. テキスト表示
st.header("1. テキスト表示")
st.write("普通のテキスト")
st.markdown("**太字**や*斜体*も使える")

# 2. データフレーム
st.header("2. データフレーム")
df = pd.DataFrame({
    '列1': [1, 2, 3, 4],
    '列2': [10, 20, 30, 40]
})
st.dataframe(df)

# 3. グラフ
st.header("3. グラフ")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# 4. ウィジェット
st.header("4. ウィジェット")

# スライダー
age = st.slider("年齢を選択", 0, 100, 25)
st.write(f"選択した年齢: {age}歳")

# セレクトボックス
option = st.selectbox(
    "好きな果物は?",
    ["りんご", "バナナ", "オレンジ"]
)
st.write(f"選択: {option}")

# チェックボックス
if st.checkbox("詳細を表示"):
    st.write("詳細情報がここに表示されます")

# 5. サイドバー
st.sidebar.header("サイドバー")
sidebar_input = st.sidebar.text_input("サイドバーの入力")

# 6. カラム
st.header("6. カラムレイアウト")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("左")
with col2:
    st.write("中央")
with col3:
    st.write("右")