Streamlit Embedding Script for EncodeCraft
This script demonstrates how to embed the EncodeCraft HTML tool into a Streamlit application.
"""

import streamlit as st
import streamlit.components.v1 as components
import os

# Page configuration
st.set_page_config(
    page_title="EncodeCraft - Advanced Encoding Tool",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better integration
st.markdown("""
    <style>
    /* Remove default padding and margin */
    .main .block-container {
        padding: 0;
        margin: 0;
        max-width: 100%;
    }
    
    /* Remove header */
    header {
        display: none !important;
    }
    
    /* Full width iframe */
    iframe {
        width: 100%;
        border: none;
        border-radius: 0;
    }
    
    /* Remove footer */
    .css-1y0tads {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔧 EncodeCraft")
st.markdown("Advanced encoding toolkit with multiple algorithms and beautiful UI")

# Method 1: Using components.html() - Recommended for static HTML
st.subheader("Method 1: Static HTML Embedding (Recommended)")

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Embed the HTML with proper sizing
components.html(
    html_content,
    height=800,
    scrolling=True
)

# Method 2: Using components.iframe() - For hosted version
st.subheader("Method 2: Iframe Embedding (For Hosted Version)")

st.code("""
# For hosted version, use:
components.iframe(
    src="https://your-domain.com/encodecraft",
    height=800,
    scrolling=True
)
""", language="python")

# Additional embedding options
with st.expander("Advanced Embedding Options"):
    st.markdown("""
    ### Custom Component Integration
    
    For more advanced integration with bidirectional communication:
    
    ```python
    import streamlit.components.v1 as components
    
    # Create a custom component
    encodecraft_component = components.declare_component(
        "encodecraft",
        url="http://localhost:3001"  # Your local dev server
    )
    
    # Use in your app
    result = encodecraft_component()
    ```
    
    ### Embedding from Different Sources
    
    1. **Local Files**: Place HTML and assets in the same directory
    2. **CDN**: Host on static hosting (Netlify, Vercel, GitHub Pages)
    3. **Base64**: Embed as data URI for single-file deployment
    
    ### Responsive Design
    
    The tool is fully responsive and will adapt to different screen sizes:
    - Desktop: Full feature set with sidebar
    - Tablet: Adjusted layout
    - Mobile: Single column stack
    """)

# Features showcase
st.subheader("✨ Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Encoding Algorithms**
    - Base64
    - URL Encoding
    - Hexadecimal
    - HTML Entities
    - ROT13
    - Binary
    """)

with col2:
    st.markdown("""
    **Modern UI**
    - Glassmorphism design
    - Dark theme
    - Smooth animations
    - Particle background
    - Responsive layout
    """)

with col3:
    st.markdown("""
    **User Experience**
    - Real-time conversion
    - Copy to clipboard
    - Conversion history
    - Keyboard shortcuts
    - Error handling
    """)

# Usage instructions
st.subheader("📖 Usage Instructions")

st.markdown("""
1. **Input Text**: Enter your text in the input textarea
2. **Select Algorithm**: Choose from the dropdown (Base64, URL, Hex, etc.)
3. **Encode/Decode**: Click the appropriate button or use keyboard shortcuts
4. **Copy Results**: Use the copy button or Ctrl+Shift+C
5. **View History**: Check the sidebar for recent conversions

### Keyboard Shortcuts
- **Ctrl/Cmd + E**: Encode
- **Ctrl/Cmd + D**: Decode  
- **Ctrl/Cmd + Shift + C**: Copy to clipboard
""")

# Technical details
with st.expander("🔧 Technical Implementation"):
    st.markdown("""
    ### Technology Stack
    - **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
    - **Styling**: Custom CSS with glassmorphism effects
    - **Animations**: Anime.js for smooth transitions
    - **Particles**: p5.js for background effects
    - **Typography**: Google Fonts (Inter + JetBrains Mono)
    - **Icons**: Font Awesome
    
    ### Browser Compatibility
    - Chrome 80+
    - Firefox 75+
    - Safari 13+
    - Edge 80+
    
    ### Performance Features
    - Debounced input handling
    - Efficient DOM updates
    - Local storage for history
    - Responsive image loading
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using modern web technologies")
