"""
Minimal Streamlit Embedding for EncodeCraft
This is the simplest way to embed the encoding tool in Streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

# Basic page setup
st.set_page_config(page_title="EncodeCraft", layout="wide")

# Title
st.title("🔧 EncodeCraft - Advanced Encoding Tool")

# Embed the HTML tool
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# This is the key line that embeds the tool
components.html(html_content, height=800, scrolling=True)

# Optional: Add some information below the tool
st.markdown("---")
st.markdown("**Features**: Base64, URL Encoding, Hexadecimal, HTML Entities, ROT13, Binary conversion")
st.markdown("**Usage**: Enter text, select algorithm, click Encode/Decode, copy results")
