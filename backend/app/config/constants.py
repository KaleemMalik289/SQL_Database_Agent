from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM Providers."""
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"

# Role Constants
SYSTEM_ROLE = "system"
USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"

# Error Messages
ERR_INVALID_SQL = "The generated SQL query is invalid or unsafe."
ERR_DB_CONNECTION = "Failed to connect to the database."
ERR_LLM_PROVIDER = "Failed to communicate with the LLM provider."
