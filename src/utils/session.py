"""
Session state management
"""

import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Input state
    if 'url_input' not in st.session_state:
        st.session_state.url_input = ""
    
    if 'urls_processed' not in st.session_state:
        st.session_state.urls_processed = []
    
    # Processing state
    if 'current_content' not in st.session_state:
        st.session_state.current_content = None
    
    if 'current_summary' not in st.session_state:
        st.session_state.current_summary = None
    
    if 'current_insights' not in st.session_state:
        st.session_state.current_insights = None
    
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = None
    
    if 'current_transformation' not in st.session_state:
        st.session_state.current_transformation = None
    
    # Settings state
    if 'summary_style' not in st.session_state:
        st.session_state.summary_style = "Executive Tone"
    
    if 'summary_depth' not in st.session_state:
        st.session_state.summary_depth = "Executive Summary"
    
    if 'processing_mode' not in st.session_state:
        st.session_state.processing_mode = "Balanced"
    
    # Multi-URL comparison
    if 'comparison_urls' not in st.session_state:
        st.session_state.comparison_urls = []
    
    if 'comparison_result' not in st.session_state:
        st.session_state.comparison_result = None
    
    # Export state
    if 'export_ready' not in st.session_state:
        st.session_state.export_ready = False

def reset_content_state():
    """Reset content-related state"""
    st.session_state.current_content = None
    st.session_state.current_summary = None
    st.session_state.current_insights = None
    st.session_state.current_questions = None
    st.session_state.current_transformation = None
    st.session_state.export_ready = False

def add_processed_url(url: str):
    """Add URL to processed list"""
    if url not in st.session_state.urls_processed:
        st.session_state.urls_processed.append(url)
        # Keep only last 10
        if len(st.session_state.urls_processed) > 10:
            st.session_state.urls_processed = st.session_state.urls_processed[-10:]
