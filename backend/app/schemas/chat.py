from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Schema for validating incoming chat requests from the frontend.
    """
    message: str = Field(
        ..., 
        min_length=2, 
        max_length=500,
        description="The natural language question from the user."
    )
    # session_id for future multi-turn conversational memory tracking
    session_id: str = Field(
        default="default-session", 
        description="Unique identifier for the chat session."
    )
