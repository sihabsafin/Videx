"""
GenAI Video & Website Content Intelligence Platform
Production-Ready SaaS Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.pages import render_main_page
from ui.sidebar import render_sidebar
from ui.theme import apply_custom_css
from utils.session import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="Content Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom styling
    apply_custom_css()
    
    # Render sidebar controls
    render_sidebar()
    
    # Render main content area
    render_main_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "Built with ❤️ using Streamlit | Powered by AI"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
