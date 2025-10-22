import streamlit as st

# 设置页面标题
st.set_page_config(page_title="HTML Viewer", layout="wide")

# 标题
st.title("📄 查看上传的 HTML 文件")

# 读取 HTML 文件
html_file = "Untitled.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 使用 Streamlit 显示 HTML 内容
st.components.v1.html(html_content, height=800, scrolling=True)
