"""
Summarization engine with multiple strategies
"""

from typing import List, Dict, Optional
from src.llm.provider import LLMProvider
from src.processors.text_processor import TextProcessor

class SummarizationEngine:
    """Multi-strategy summarization engine"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.processor = TextProcessor()
    
    def summarize(self, 
                  content: str, 
                  depth: str = "Executive Summary",
                  style: str = "Executive Tone",
                  source_type: str = "website") -> str:
        """
        Main summarization method
        
        Args:
            content: Text to summarize
            depth: Summary depth (TL;DR, Bullet Points, etc.)
            style: Writing style
            source_type: 'youtube' or 'website'
        """
        # Choose strategy based on content length
        token_count = self.processor.count_tokens(content)
        
        if token_count < 4000:
            # Single-pass summarization
            return self._stuff_summarize(content, depth, style)
        elif token_count < 15000:
            # Refine strategy
            return self._refine_summarize(content, depth, style)
        else:
            # Map-reduce for very long content
            return self._map_reduce_summarize(content, depth, style)
    
    def _stuff_summarize(self, content: str, depth: str, style: str) -> str:
        """Single-pass summarization for short content"""
        instruction = self._get_instruction(depth, style)
        
        return self.llm.generate_with_context(
            context=content,
            instruction=instruction,
            style=style
        )
    
    def _refine_summarize(self, content: str, depth: str, style: str) -> str:
        """Iterative refinement for medium content"""
        chunks = self.processor.chunk_text(content)
        
        # First pass: summarize first chunk
        instruction = self._get_instruction(depth, style)
        current_summary = self.llm.generate_with_context(
            context=chunks[0]['text'],
            instruction=instruction,
            style=style
        )
        
        # Subsequent passes: refine with additional chunks
        for chunk in chunks[1:]:
            refine_instruction = f"""{instruction}

Previous summary:
{current_summary}

Additional content:
{chunk['text']}

Refine and expand the previous summary to incorporate this new information."""
            
            current_summary = self.llm.generate(refine_instruction)
        
        return current_summary
    
    def _map_reduce_summarize(self, content: str, depth: str, style: str) -> str:
        """Map-reduce for very long content"""
        chunks = self.processor.chunk_text(content)
        
        # Map: Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            instruction = f"Summarize the following content concisely, preserving key points:\n\n{chunk['text']}"
            summary = self.llm.generate(instruction)
            chunk_summaries.append(summary)
        
        # Reduce: Combine summaries
        combined = "\n\n".join(chunk_summaries)
        instruction = self._get_instruction(depth, style)
        
        return self.llm.generate_with_context(
            context=combined,
            instruction=instruction,
            style=style
        )
    
    def _get_instruction(self, depth: str, style: str) -> str:
        """Generate instruction based on depth and style"""
        instructions = {
            "TL;DR (1-2 lines)": "Provide a 1-2 sentence TL;DR summary.",
            "Bullet Points": "Create a bullet-point summary with 5-8 key points.",
            "Executive Summary": "Write a concise executive summary (2-3 paragraphs) highlighting main points and insights.",
            "Detailed Summary": "Provide a comprehensive summary covering all major points, arguments, and details.",
            "Structured Outline": "Create a structured outline with main sections, sub-points, and key details."
        }
        
        base_instruction = instructions.get(depth, instructions["Executive Summary"])
        
        # Add style modifiers
        style_modifiers = {
            "Simple Explanation": "Use simple language suitable for a general audience.",
            "Technical Explanation": "Use technical terminology and detailed explanations.",
            "Academic Tone": "Write in an academic, scholarly tone with formal language.",
            "Executive Tone": "Write in a professional, executive-level tone.",
            "Casual Tone": "Use a conversational, casual tone.",
            "LinkedIn Post": "Format as an engaging LinkedIn post with appropriate hashtags.",
            "Twitter Thread": "Format as a Twitter thread (multiple connected tweets)."
        }
        
        modifier = style_modifiers.get(style, "")
        
        return f"{base_instruction} {modifier}".strip()
    
    def extract_insights(self, content: str) -> str:
        """Extract key insights, arguments, and claims"""
        instruction = """Analyze this content and extract:

1. Key Ideas: Main concepts and themes
2. Arguments: Primary arguments made
3. Evidence: Supporting evidence provided
4. Implications: What this means or suggests
5. Limitations: Any gaps or limitations noted

Be specific and cite relevant points."""
        
        return self.llm.generate_with_context(
            context=content,
            instruction=instruction
        )
    
    def generate_questions(self, content: str, question_type: str = "study") -> str:
        """Generate questions from content"""
        instructions = {
            "study": "Generate 10 study questions that test understanding of this content.",
            "discussion": "Generate 5 thought-provoking discussion questions.",
            "interview": "Generate potential interview questions based on this content.",
            "mcq": "Generate 5 multiple-choice questions with 4 options each (mark correct answer)."
        }
        
        instruction = instructions.get(question_type, instructions["study"])
        
        return self.llm.generate_with_context(
            context=content,
            instruction=instruction
        )
    
    def transform_content(self, content: str, format_type: str) -> str:
        """Transform content into different formats"""
        instructions = {
            "blog": "Transform this into a well-structured blog post with introduction, body sections, and conclusion.",
            "linkedin": "Create an engaging LinkedIn post (max 1300 characters) with relevant hashtags.",
            "email": "Draft a professional email summarizing this content.",
            "meeting_notes": "Format this as structured meeting notes with action items.",
            "notion": "Create a Notion-style structured document with headers, sections, and bullet points."
        }
        
        instruction = instructions.get(format_type, instructions["blog"])
        
        return self.llm.generate_with_context(
            context=content,
            instruction=instruction
        )
    
    def compare_sources(self, sources: List[Dict[str, str]]) -> str:
        """Compare multiple sources"""
        # Format sources
        formatted_sources = []
        for i, source in enumerate(sources, 1):
            formatted_sources.append(
                f"Source {i} ({source['url']}):\n{source['content'][:2000]}"
            )
        
        combined = "\n\n---\n\n".join(formatted_sources)
        
        instruction = """Compare these sources and provide:

1. Common Themes: What ideas appear across multiple sources?
2. Differing Viewpoints: Where do sources disagree?
3. Unique Insights: What unique points does each source make?
4. Synthesis: What conclusions can be drawn from all sources together?

Create a comparison table format where possible."""
        
        return self.llm.generate_with_context(
            context=combined,
            instruction=instruction
        )
