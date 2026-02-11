"""
Sidebar UI component
"""

import streamlit as st
from src.config import Config

def render_sidebar():
    """Render sidebar with settings and controls"""
    
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # API Configuration Status
        st.markdown("### 🔑 API Status")
        if Config.is_configured():
            provider = Config.get_available_provider()
            st.success(f"✅ Connected: {provider.upper()}")
        else:
            st.error("❌ No API keys configured")
            st.info("Add API keys to .env file")
        
        st.markdown("---")
        
        # Processing Settings
        st.markdown("### 🎯 Processing")
        
        st.session_state.processing_mode = st.selectbox(
            "Mode",
            Config.PROCESSING_MODES,
            index=Config.PROCESSING_MODES.index(st.session_state.processing_mode),
            help="Fast: Quick results | Balanced: Good quality | Accurate: Best quality"
        )
        
        st.session_state.summary_depth = st.selectbox(
            "Summary Depth",
            Config.SUMMARY_DEPTHS,
            index=Config.SUMMARY_DEPTHS.index(st.session_state.summary_depth)
        )
        
        st.session_state.summary_style = st.selectbox(
            "Writing Style",
            Config.SUMMARY_STYLES,
            index=Config.SUMMARY_STYLES.index(st.session_state.summary_style)
        )
        
        st.markdown("---")
        
        # Usage Stats
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("URLs Processed", len(st.session_state.urls_processed))
        
        with col2:
            comparison_count = len(st.session_state.comparison_urls)
            st.metric("Comparisons", comparison_count)
        
        # Recent URLs
        if st.session_state.urls_processed:
            st.markdown("### 📚 Recent")
            for url in st.session_state.urls_processed[-3:]:
                # Truncate long URLs
                display_url = url if len(url) < 40 else url[:37] + "..."
                st.text(display_url)
        
        st.markdown("---")
        
        # About
        st.markdown("### ℹ️ About")
        st.markdown("""
        This platform uses advanced AI to:
        - Extract content from videos & websites
        - Generate multi-level summaries
        - Extract key insights
        - Transform content formats
        - Compare multiple sources
        """)
        
        st.markdown("---")
        st.markdown("Built with Streamlit + LangChain")
