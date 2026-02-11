"""
Text preprocessing and intelligent chunking
"""

import tiktoken
from typing import List, Dict
import re

class TextProcessor:
    """Process and chunk text for LLM consumption"""
    
    def __init__(self, max_chunk_size: int = 8000, overlap: int = 500):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Remove multiple newlines (but keep paragraph structure)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove special characters that might confuse LLM
        text = text.replace('\r', '\n')
        text = text.replace('\t', ' ')
        
        # Remove URLs (optional - might want to keep for context)
        # text = re.sub(r'http[s]?://\S+', '[URL]', text)
        
        return text.strip()
    
    def split_by_sections(self, text: str) -> List[str]:
        """
        Try to split text by natural sections (headings, paragraphs)
        """
        # Try to detect section breaks
        # Common patterns: lines ending with ":", standalone short lines, etc.
        
        sections = []
        current_section = []
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            current_section.append(line)
            
            # Check if this might be a section break
            if (
                line.endswith(':') or  # Heading-like
                (len(line) < 50 and i < len(lines) - 1 and lines[i+1] == '') or  # Short line before blank
                line.strip() == ''  # Blank line
            ):
                if current_section:
                    section_text = '\n'.join(current_section).strip()
                    if section_text:
                        sections.append(section_text)
                    current_section = []
        
        # Add remaining
        if current_section:
            section_text = '\n'.join(current_section).strip()
            if section_text:
                sections.append(section_text)
        
        return sections if sections else [text]
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        """
        Intelligently chunk text with overlap
        Returns list of chunks with metadata
        """
        text = self.clean_text(text)
        
        # If text is small enough, return as single chunk
        token_count = self.count_tokens(text)
        if token_count <= self.max_chunk_size:
            return [{
                'text': text,
                'chunk_id': 0,
                'total_chunks': 1,
                'token_count': token_count
            }]
        
        # Split into sections first
        sections = self.split_by_sections(text)
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        chunk_id = 0
        
        for section in sections:
            section_tokens = self.count_tokens(section)
            
            # If single section is too large, split it
            if section_tokens > self.max_chunk_size:
                # Split by sentences
                sentences = re.split(r'(?<=[.!?])\s+', section)
                
                for sentence in sentences:
                    sentence_tokens = self.count_tokens(sentence)
                    
                    if current_tokens + sentence_tokens > self.max_chunk_size:
                        # Save current chunk
                        if current_chunk:
                            chunks.append({
                                'text': current_chunk.strip(),
                                'chunk_id': chunk_id,
                                'token_count': current_tokens
                            })
                            chunk_id += 1
                            
                            # Start new chunk with overlap
                            overlap_text = self._get_overlap(current_chunk)
                            current_chunk = overlap_text + " " + sentence
                            current_tokens = self.count_tokens(current_chunk)
                        else:
                            current_chunk = sentence
                            current_tokens = sentence_tokens
                    else:
                        current_chunk += " " + sentence
                        current_tokens += sentence_tokens
            
            # Section fits in current chunk
            elif current_tokens + section_tokens <= self.max_chunk_size:
                current_chunk += "\n\n" + section
                current_tokens += section_tokens
            
            # Section doesn't fit, start new chunk
            else:
                if current_chunk:
                    chunks.append({
                        'text': current_chunk.strip(),
                        'chunk_id': chunk_id,
                        'token_count': current_tokens
                    })
                    chunk_id += 1
                
                current_chunk = section
                current_tokens = section_tokens
        
        # Add final chunk
        if current_chunk:
            chunks.append({
                'text': current_chunk.strip(),
                'chunk_id': chunk_id,
                'token_count': current_tokens
            })
        
        # Add total chunks to each
        total = len(chunks)
        for chunk in chunks:
            chunk['total_chunks'] = total
        
        return chunks
    
    def _get_overlap(self, text: str) -> str:
        """Get last N tokens for overlap"""
        tokens = self.encoding.encode(text)
        overlap_tokens = tokens[-self.overlap:] if len(tokens) > self.overlap else tokens
        return self.encoding.decode(overlap_tokens)
    
    def extract_key_sentences(self, text: str, n: int = 5) -> List[str]:
        """Extract potentially key sentences (simple heuristic)"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Simple scoring: longer sentences, sentences with important keywords
        scored = []
        keywords = ['important', 'key', 'main', 'critical', 'essential', 'conclusion', 'summary']
        
        for sent in sentences:
            score = len(sent)  # Length bonus
            for kw in keywords:
                if kw in sent.lower():
                    score += 100
            scored.append((score, sent))
        
        scored.sort(reverse=True)
        return [sent for _, sent in scored[:n]]
