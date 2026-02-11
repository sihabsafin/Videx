"""
Custom CSS for modern, professional UI
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        background-color: #0f172a;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .app-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .custom-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #6366f1;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .custom-card h3 {
        color: #f1f5f9;
        margin-top: 0;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #1e3a5f;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #1e3a2f;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #3a2e1e;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #3a1e1e;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #1e293b;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94a3b8;
        font-weight: 500;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6366f1;
        color: white;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 2px solid #334155;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #1e293b;
        color: #f1f5f9;
        border-radius: 6px;
    }
    
    /* Markdown content */
    .markdown-content {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #334155;
        margin: 1rem 0;
    }
    
    /* Metrics */
    .metric-card {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e293b;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #6366f1;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e293b;
        color: #f1f5f9;
        border-radius: 6px;
    }
    
    /* Toast notifications */
    .stToast {
        background-color: #1e293b;
        border-radius: 8px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render app header"""
    st.markdown("""
    <div class="app-header">
        <h1>🧠 Content Intelligence Platform</h1>
        <p>AI-powered content analysis for YouTube videos and websites</p>
    </div>
    """, unsafe_allow_html=True)

def render_info_box(message: str, box_type: str = "info"):
    """Render styled info box"""
    box_classes = {
        "info": "info-box",
        "success": "success-box",
        "warning": "warning-box",
        "error": "error-box"
    }
    
    st.markdown(f"""
    <div class="{box_classes.get(box_type, 'info-box')}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def render_metric(label: str, value: str):
    """Render metric card"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)
