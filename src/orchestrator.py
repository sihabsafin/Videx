"""
Content processing orchestrator
Coordinates extraction, processing, and summarization
"""

from typing import Dict, Optional
from src.extractors.youtube_extractor import YouTubeExtractor
from src.extractors.website_extractor import WebsiteExtractor
from src.processors.text_processor import TextProcessor
from src.engines.summarization import SummarizationEngine
from src.llm.provider import LLMProvider
from src.utils.url_validator import URLValidator

class ContentOrchestrator:
    """Orchestrates the entire content processing pipeline"""
    
    def __init__(self, processing_mode: str = "balanced"):
        self.processing_mode = processing_mode
        self.youtube_extractor = YouTubeExtractor()
        self.website_extractor = WebsiteExtractor()
        self.text_processor = TextProcessor()
        
        # Initialize LLM
        self.llm_provider = LLMProvider(provider="auto", mode=processing_mode.lower())
        self.summarization_engine = SummarizationEngine(self.llm_provider)
    
    def process_url(self, url: str) -> Dict:
        """
        Main processing pipeline
        
        Returns: {
            'success': bool,
            'source_type': str,
            'title': str,
            'content': str,
            'metadata': dict,
            'error': Optional[str]
        }
        """
        # Validate URL
        is_valid, error = URLValidator.validate_url(url)
        if not is_valid:
            return {
                'success': False,
                'error': error
            }
        
        # Detect source type
        source_type = URLValidator.detect_source_type(url)
        
        # Extract content
        if source_type == 'youtube':
            return self._process_youtube(url)
        else:
            return self._process_website(url)
    
    def _process_youtube(self, url: str) -> Dict:
        """Process YouTube video"""
        video_id = self.youtube_extractor.extract_video_id(url)
        
        if not video_id:
            return {
                'success': False,
                'error': 'Invalid YouTube URL'
            }
        
        # Extract transcript
        result = self.youtube_extractor.get_transcript(video_id)
        
        if not result['success']:
            return {
                'success': False,
                'error': result['error']
            }
        
        # Process content
        content = self.text_processor.clean_text(result['content'])
        
        return {
            'success': True,
            'source_type': 'youtube',
            'title': f"YouTube Video: {video_id}",
            'content': content,
            'metadata': {
                'video_id': video_id,
                'has_timestamps': True,
                'sections': result.get('sections', []),
                'token_count': self.text_processor.count_tokens(content)
            },
            'error': None
        }
    
    def _process_website(self, url: str) -> Dict:
        """Process website"""
        result = self.website_extractor.extract_content(url)
        
        if not result['success']:
            return {
                'success': False,
                'error': result['error']
            }
        
        # Process content
        content = self.text_processor.clean_text(result['content'])
        
        return {
            'success': True,
            'source_type': 'website',
            'title': result.get('title', 'Untitled'),
            'content': content,
            'metadata': {
                'url': url,
                'token_count': self.text_processor.count_tokens(content)
            },
            'error': None
        }
    
    def generate_summary(self, 
                        content: str, 
                        depth: str,
                        style: str,
                        source_type: str = 'website') -> str:
        """Generate summary"""
        return self.summarization_engine.summarize(
            content=content,
            depth=depth,
            style=style,
            source_type=source_type
        )
    
    def generate_insights(self, content: str) -> str:
        """Generate insights"""
        return self.summarization_engine.extract_insights(content)
    
    def generate_questions(self, content: str, question_type: str = "study") -> str:
        """Generate questions"""
        return self.summarization_engine.generate_questions(content, question_type)
    
    def transform_content(self, content: str, format_type: str) -> str:
        """Transform content"""
        return self.summarization_engine.transform_content(content, format_type)
    
    def compare_urls(self, urls: list) -> str:
        """Compare multiple URLs"""
        sources = []
        
        for url in urls:
            result = self.process_url(url)
            if result['success']:
                sources.append({
                    'url': url,
                    'content': result['content'][:3000]  # Limit content
                })
        
        if not sources:
            return "No valid sources to compare"
        
        return self.summarization_engine.compare_sources(sources)
    
    def get_llm_info(self) -> Dict:
        """Get LLM provider info"""
        return self.llm_provider.get_info()
