# 复制下面这段代码（只有 8 行）
import streamlit as st
st.title("나만의 웹")
score = st.sidebar.slider("점수", 0, 1000, 750)
st.write(f"점수: {score}")
if st.button("결과"):
    st.success("✅ 성공!")
