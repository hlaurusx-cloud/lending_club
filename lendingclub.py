import pandas as pd
import streamlit as st
import numpy as np

# ---------- 页面设置 ----------
st.set_page_config(page_title="Finance Credit Dashboard", page_icon="📊", layout="wide")

# ---------- CSS 注入（Finance 风格） ----------
st.markdown(
    """
    <style>
    /* 背景 */
    .main {
        background: linear-gradient(135deg, #1e2a3a, #2c3e50);
        color: #ecf0f1;
        font-family: 'Segoe UI', sans-serif;
    }
    /* 卡片 */
    .card {
        background-color: #283747;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    /* 指标文字 */
    .metric {
        font-size: 2rem;
        font-weight: bold;
        color: #1abc9c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 顶部标题 ----------
st.title("📊 Finance Credit Dashboard")
st.markdown("---")

# ---------- 侧边栏（导航 + 控制） ----------
st.sidebar.header("Control Panel")
user_name = st.sidebar.text_input("User Name", "James")
score = st.sidebar.slider("Credit Score", 300, 850, 750)
theme_color = st.sidebar.color_picker("Accent Color", "#1abc9c")

# ---------- 顶部 KPI 卡片 ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="card"><span class="metric">{score}</span><br>Credit Score</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="card"><span class="metric">{"Excellent" if score >= 800 else "Good" if score >= 700 else "Fair"}</span><br>Rating</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="card"><span class="metric">{np.random.randint(1, 10)}</span><br>Inquiries</div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="card"><span class="metric">{np.random.randint(1, 50)}</span><br>Delinq</div>', unsafe_allow_html=True)

# ---------- 图表区 ----------
left, right = st.columns([2, 1])

with left:
    st.subheader("📈 Score Trend (Fake)")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    values = [score + np.random.randint(-30, 30) for _ in months]
    st.line_chart(pd.DataFrame({"Month": months, "Score": values}).set_index("Month"))

with right:
    st.subheader("📧 Recent Alerts")
    alerts = [
        "Hooray! Your score increased by 12 pts.",
        "Payment due in 3 days.",
        "New inquiry detected.",
    ]
    for a in alerts:
        st.info(a)

# ---------- 底部按钮 ----------
st.markdown("---")
if st.button("🎲 Simulate New Month"):
    st.balloons()
    st.success(f"New score: {np.random.randint(650, 850)}")
