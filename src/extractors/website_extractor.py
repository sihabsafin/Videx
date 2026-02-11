"""
Website content extraction using BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class WebsiteExtractor:
    """Extract clean content from websites"""
    
    # Tags to remove (ads, scripts, navigation, etc.)
    REMOVE_TAGS = [
        'script', 'style', 'nav', 'header', 'footer', 
        'aside', 'iframe', 'noscript', 'svg'
    ]
    
    # Tags that typically contain ads or irrelevant content
    REMOVE_CLASSES = [
        'ad', 'advertisement', 'promo', 'sidebar', 'related',
        'popup', 'modal', 'newsletter', 'subscribe', 'social'
    ]
    
    @staticmethod
    def extract_content(url: str) -> Dict:
        """
        Extract main content from website
        Returns: {
            'success': bool,
            'content': str,
            'title': Optional[str],
            'error': Optional[str]
        }
        """
        try:
            # Fetch page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = None
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            
            # Remove unwanted tags
            for tag in WebsiteExtractor.REMOVE_TAGS:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Remove elements with ad-related classes
            for element in soup.find_all(class_=re.compile('|'.join(WebsiteExtractor.REMOVE_CLASSES), re.I)):
                element.decompose()
            
            # Try to find main content
            main_content = None
            
            # Strategy 1: Look for <article> tag
            article = soup.find('article')
            if article:
                main_content = article
            
            # Strategy 2: Look for main content containers
            if not main_content:
                for tag in ['main', 'div']:
                    for class_name in ['content', 'main-content', 'article', 'post', 'entry']:
                        element = soup.find(tag, class_=re.compile(class_name, re.I))
                        if element:
                            main_content = element
                            break
                    if main_content:
                        break
            
            # Strategy 3: Use body if nothing else found
            if not main_content:
                main_content = soup.find('body')
            
            if not main_content:
                return {
                    'success': False,
                    'content': None,
                    'title': None,
                    'error': "Could not extract main content from page"
                }
            
            # Extract and clean text
            text = main_content.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            
            # Remove excessive whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            # Basic validation
            if len(text) < 100:
                return {
                    'success': False,
                    'content': None,
                    'title': title,
                    'error': "Extracted content too short (possible paywall or extraction issue)"
                }
            
            return {
                'success': True,
                'content': text,
                'title': title,
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'content': None,
                'error': "Request timeout - website took too long to respond"
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'content': None,
                'error': f"Failed to fetch website: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'error': f"Error extracting content: {str(e)}"
            }
    
    @staticmethod
    def extract_headings(content: str) -> list:
        """Extract potential section headings from content"""
        lines = content.split('\n')
        headings = []
        
        for line in lines:
            # Heuristic: short lines (< 100 chars) that end with : or are title case
            if len(line) < 100 and (line.endswith(':') or line.istitle()):
                headings.append(line)
        
        return headings[:20]  # Limit to first 20
