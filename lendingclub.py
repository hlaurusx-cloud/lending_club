import streamlit as st
import numpy as np
import pandas as pd

# ---------- 页面配置 ----------
st.set_page_config(page_title="Neon Credit Dashboard", page_icon="💠", layout="wide")

# ---------- CSS 注入（暗黑科技 + 霓虹） ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .main {
        background: #0d0d0d;
        color: #e0e0e0;
        font-family: 'Orbitron', sans-serif;
    }
    .neon-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid #00ffea;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 0 20px #00ffea;
        margin-bottom: 1rem;
    }
    .neon-text {
        font-size: 2.5rem;
        color: #00ffea;
        text-shadow: 0 0 10px #00ffea;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 顶部标题 ----------
st.title("💠 Neon Credit Dashboard")
st.markdown("---")

# ---------- 侧边栏 ----------
st.sidebar.header("🎛️ Control")
user_name = st.sidebar.text_input("User Name", "CyberUser")
score = st.sidebar.slider("Credit Score", 300, 850, 750)
accent = st.sidebar.color_picker("Neon Color", "#00ffea")

# ---------- 霓虹 KPI ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="neon-card"><span class="neon-text">{score}</span><br>Score</div>', unsafe_allow_html=True)
with col2:
    rating = "EXCELLENT" if score >= 800 else "GOOD" if score >= 700 else "FAIR"
    st.markdown(f'<div class="neon-card"><span style="font-size:2rem;color:{accent};">{rating}</span><br>Rating</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="neon-card"><span style="font-size:2rem;color:{accent};">{np.random.randint(1,10)}</span><br>Inquiries</div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="neon-card"><span style="font-size:2rem;color:{accent};">{np.random.randint(1,50)}</span><br>Delinq</div>', unsafe_allow_html=True)

# ---------- 霓虹折线 ----------
st.subheader("📈 Score Trend")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
values = [score + np.random.randint(-30, 30) for _ in months]
chart_data = pd.DataFrame({"Month": months, "Score": values})
st.line_chart(chart_data.set_index("Month"))

# ---------- 霓虹按钮 ----------
st.markdown("---")
if st.button("🎲 Generate New Score"):
    st.balloons()
    new_score = np.random.randint(650, 850)
    st.success(f"✨ New Score: **{new_score}**")
