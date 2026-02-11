"""
URL validation and type detection utilities
"""

import re
from urllib.parse import urlparse
from typing import Tuple, Optional

class URLValidator:
    """Validate and categorize URLs"""
    
    YOUTUBE_PATTERNS = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
    ]
    
    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL and return (is_valid, error_message)
        """
        if not url or not url.strip():
            return False, "Please enter a URL"
        
        url = url.strip()
        
        # Check basic URL structure
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False, "Invalid URL format. Must include http:// or https://"
        except Exception:
            return False, "Invalid URL format"
        
        # Check scheme
        if result.scheme not in ['http', 'https']:
            return False, "URL must start with http:// or https://"
        
        return True, None
    
    @classmethod
    def detect_source_type(cls, url: str) -> str:
        """
        Detect if URL is YouTube video or website
        Returns: 'youtube' or 'website'
        """
        for pattern in cls.YOUTUBE_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return 'youtube'
        
        return 'website'
    
    @classmethod
    def extract_video_id(cls, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        for pattern in cls.YOUTUBE_PATTERNS:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    @classmethod
    def is_valid_domain(cls, url: str) -> bool:
        """Check if domain seems legitimate"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Blocked patterns (malicious, spam, etc.)
            blocked_patterns = [
                'localhost',
                '127.0.0.1',
                'file://',
            ]
            
            for pattern in blocked_patterns:
                if pattern in domain:
                    return False
            
            return True
        except:
            return False
