"""
Configuration management for the application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    DEFAULT_MODEL = "groq"  # or "gemini"
    
    GROQ_MODELS = {
        "fast": "llama-3.1-8b-instant",
        "balanced": "llama-3.1-70b-versatile",
        "accurate": "llama-3.1-70b-versatile"
    }
    
    GEMINI_MODELS = {
        "fast": "gemini-1.5-flash",
        "balanced": "gemini-1.5-flash",
        "accurate": "gemini-1.5-pro"
    }
    
    # Processing Configuration
    MAX_CHUNK_SIZE = 8000
    CHUNK_OVERLAP = 500
    MAX_VIDEO_LENGTH = 10800  # 3 hours in seconds
    
    # Rate Limiting
    MAX_URLS_PER_SESSION = 10
    MAX_COMPARISON_URLS = 5
    
    # Export Configuration
    EXPORT_FORMATS = ["PDF", "Markdown", "Plain Text"]
    
    # UI Configuration
    SUMMARY_STYLES = [
        "Simple Explanation",
        "Technical Explanation",
        "Academic Tone",
        "Executive Tone",
        "Casual Tone",
        "LinkedIn Post",
        "Twitter Thread"
    ]
    
    SUMMARY_DEPTHS = [
        "TL;DR (1-2 lines)",
        "Bullet Points",
        "Executive Summary",
        "Detailed Summary",
        "Structured Outline"
    ]
    
    PROCESSING_MODES = ["Fast", "Balanced", "Accurate"]
    
    @classmethod
    def is_configured(cls):
        """Check if API keys are configured"""
        return bool(cls.GROQ_API_KEY or cls.GOOGLE_API_KEY)
    
    @classmethod
    def get_available_provider(cls):
        """Get the first available provider"""
        if cls.GROQ_API_KEY:
            return "groq"
        elif cls.GOOGLE_API_KEY:
            return "gemini"
        return None
