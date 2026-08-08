from pydantic import BaseModel, Field
from typing import Any, Optional

class APIResponse(BaseModel):
    """
    Standardized wrapper for ALL API responses across the backend.
    Ensures the frontend has a predictable contract: { success, message, data, error }
    """
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
