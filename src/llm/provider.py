"""
LLM provider abstraction layer
Supports Groq and Google Gemini
"""

from typing import Optional, Dict
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from src.config import Config

class LLMProvider:
    """Unified interface for different LLM providers"""
    
    def __init__(self, provider: str = "auto", mode: str = "balanced"):
        """
        Initialize LLM provider
        
        Args:
            provider: "groq", "gemini", or "auto" (use first available)
            mode: "fast", "balanced", or "accurate"
        """
        self.provider = provider
        self.mode = mode
        self.llm = None
        
        # Auto-detect provider if needed
        if provider == "auto":
            self.provider = Config.get_available_provider()
            if not self.provider:
                raise ValueError("No API keys configured. Please set GROQ_API_KEY or GOOGLE_API_KEY")
        
        # Initialize LLM
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM"""
        if self.provider == "groq":
            model = Config.GROQ_MODELS.get(self.mode, Config.GROQ_MODELS["balanced"])
            self.llm = ChatGroq(
                api_key=Config.GROQ_API_KEY,
                model_name=model,
                temperature=0.3,
                max_tokens=4000
            )
        
        elif self.provider == "gemini":
            model = Config.GEMINI_MODELS.get(self.mode, Config.GEMINI_MODELS["balanced"])
            self.llm = ChatGoogleGenerativeAI(
                api_key=Config.GOOGLE_API_KEY,
                model=model,
                temperature=0.3,
                max_output_tokens=4000
            )
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    def generate_with_context(self, 
                            context: str, 
                            instruction: str, 
                            style: Optional[str] = None) -> str:
        """
        Generate response with context and instruction
        
        Args:
            context: Background context/content
            instruction: What to do with the context
            style: Optional style modifier
            
        Returns:
            Generated text
        """
        system_prompt = "You are an expert content analyst and summarizer."
        
        if style:
            system_prompt += f" Provide your response in a {style} style."
        
        prompt = f"""Content:
{context}

Task:
{instruction}

Provide a clear, accurate, and well-structured response."""
        
        return self.generate(prompt, system_prompt)
    
    def get_info(self) -> Dict[str, str]:
        """Get provider information"""
        model = ""
        if self.provider == "groq":
            model = Config.GROQ_MODELS.get(self.mode, "unknown")
        elif self.provider == "gemini":
            model = Config.GEMINI_MODELS.get(self.mode, "unknown")
        
        return {
            "provider": self.provider,
            "mode": self.mode,
            "model": model
        }
