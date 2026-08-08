from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class LLMProviderFactory:
    """
    Factory class to initialize and return the appropriately configured LLM.
    Ensures the LLM is initialized only once (Singleton pattern) and abstracts
    the provider logic away from the business layer.
    """
    _instance: BaseChatModel = None

    @classmethod
    def get_llm(cls) -> BaseChatModel:
        if cls._instance is not None:
            return cls._instance

        provider = settings.DEFAULT_LLM_PROVIDER.upper()
        
        logger.info(f"Initializing LLM Provider: {provider}")

        if provider == "GROQ":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is not set in environment variables.")
            
            primary_llm = ChatGroq(
                temperature=0,
                groq_api_key=settings.GROQ_API_KEY,
                model_name="llama-3.3-70b-versatile",
                max_tokens=2048,
                model_kwargs={"top_p": 0.9}
            )
            
            # Fallback 1: If 70b hits rate limits, drop down to the ultra-fast 8b model
            fallback_1 = ChatGroq(
                temperature=0,
                groq_api_key=settings.GROQ_API_KEY,
                model_name="llama3-8b-8192",
                max_tokens=2048,
                model_kwargs={"top_p": 0.9}
            )
            
            # Fallback 2: If both llamas are exhausted, use Mixtral
            fallback_2 = ChatGroq(
                temperature=0,
                groq_api_key=settings.GROQ_API_KEY,
                model_name="mixtral-8x7b-32768",
                max_tokens=2048,
                model_kwargs={"top_p": 0.9}
            )
            
            # Chain them together so rate-limit crashes transparently failover to the next model
            cls._instance = primary_llm.with_fallbacks([fallback_1, fallback_2])
            
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        return cls._instance

def get_llm() -> BaseChatModel:
    """Convenience function to get the LLM instance."""
    return LLMProviderFactory.get_llm()
