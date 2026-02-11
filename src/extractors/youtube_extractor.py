"""
YouTube content extraction using youtube-transcript-api
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from typing import Dict, List, Optional
import re

class YouTubeExtractor:
    """Extract transcripts and metadata from YouTube videos"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_transcript(video_id: str) -> Dict:
        """
        Get transcript with timestamps
        Returns: {
            'success': bool,
            'content': str,
            'transcript_with_timestamps': List[Dict],
            'error': Optional[str]
        }
        """
        try:
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format content
            full_text = " ".join([entry['text'] for entry in transcript_list])
            
            # Create timestamped sections (every ~5 minutes)
            timestamped_sections = []
            current_section = {
                'start_time': 0,
                'text': '',
                'duration': 0
            }
            
            section_duration = 300  # 5 minutes
            
            for entry in transcript_list:
                if entry['start'] - current_section['start_time'] >= section_duration:
                    if current_section['text']:
                        timestamped_sections.append(current_section)
                    current_section = {
                        'start_time': entry['start'],
                        'text': entry['text'],
                        'duration': entry['duration']
                    }
                else:
                    current_section['text'] += ' ' + entry['text']
                    current_section['duration'] += entry['duration']
            
            # Add last section
            if current_section['text']:
                timestamped_sections.append(current_section)
            
            return {
                'success': True,
                'content': full_text,
                'transcript_with_timestamps': transcript_list,
                'sections': timestamped_sections,
                'error': None
            }
            
        except TranscriptsDisabled:
            return {
                'success': False,
                'content': None,
                'error': "Transcripts are disabled for this video"
            }
        except NoTranscriptFound:
            return {
                'success': False,
                'content': None,
                'error': "No transcript found for this video"
            }
        except Exception as e:
            return {
                'success': False,
                'content': None,
                'error': f"Error extracting transcript: {str(e)}"
            }
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Format seconds to HH:MM:SS or MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def get_section_summaries_context(sections: List[Dict]) -> str:
        """Format sections for LLM context"""
        formatted = []
        for i, section in enumerate(sections, 1):
            timestamp = YouTubeExtractor.format_timestamp(section['start_time'])
            formatted.append(
                f"[{timestamp}] Section {i}:\n{section['text'][:500]}..."
            )
        return "\n\n".join(formatted)
