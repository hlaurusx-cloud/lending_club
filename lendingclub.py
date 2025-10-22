import streamlit as st
import numpy as np

# 🎨 页面配置
st.set_page_config(
    page_title="신용평가 디자인",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🌈 CSS 注入（背景渐变 + 字体）
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #ffeef8, #e8f4ff);
        font-family: 'Apple SD Gothic Neo', sans-serif;
    }
    h1, h2, h3 {
        color: #4a4a8a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✨ 标题区
st.title("✨ 나만의 신용평가 시스템")
st.markdown("> **디자인 먼저!** 데이터는 나중에 🔮")

# 🧭 侧边栏 - 设计控制台
st.sidebar.header("🎛️ 디자인控制台")
theme_color = st.sidebar.color_picker("테마 색상", "#FFB6C1")
user_name = st.sidebar.text_input("당신의 이름", "아이유")
score = st.sidebar.slider("신용 점수 (0~1000)", 0, 1000, 750)

# 📊 结果卡片区
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<h3 style='color:{theme_color};'>💳 점수</h3>", unsafe_allow_html=True)
    st.metric(label="신용점수", value=score, delta=score - 700)

with col2:
    st.markdown(f"<h3 style='color:{theme_color};'>📊 등급</h3>", unsafe_allow_html=True)
    if score >= 800:
        st.success("🌟 1등급")
    elif score >= 700:
        st.info("✨ 2등급")
    else:
        st.warning("⚠️ 3등급 이하")

with col3:
    st.markdown(f"<h3 style='color:{theme_color};'>💬 한 줄 평</h3>", unsafe_allow_html=True)
    st.write(f"**{user_name}**님은 **신용왕**입니다!" if score >= 800 else "**{user_name}**님, 조금만 더 노력하세요!")

# 🎯 交互按钮
if st.button("🎲 랜덤 점수 생성"):
    new_score = np.random.randint(300, 950)
    st.balloons()
    st.success(f"🎉 새로운 점수: **{new_score}**")

# 🖼️ 图片占位区
st.markdown("---")
st.markdown("### 🌸 디자인 요소展示区")
st.image(f"https://via.placeholder.com/600x200.png/{theme_color[1:]}/FFFFFF?text=Credit+Score", use_column_width=True)

# 📱 底部
st.markdown("---")
st.markdown("💌 **Contact**: yourname@example.com | **GitHub**: [github.com/yourname](https://github.com/yourname)")
