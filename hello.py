import streamlit as st

st.title("Hello Streamlit! 👋")
st.write("これがWebアプリです")

name = st.text_input("名前を入力してください")
if name:
    st.write(f"こんにちは、{name}さん!")

if st.button("クリック!"):
    st.balloons()  # 風船が飛ぶ