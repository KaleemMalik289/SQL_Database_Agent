from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest
from app.schemas.response import APIResponse
from app.services.chat_service import ChatService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat Interface"]
)

@router.post(
    "", 
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Process a natural language SQL query",
    description="Receives a natural language question, validates it, and streams it to the LangChain SQL Agent via the Service Layer."
)
async def process_chat(request: ChatRequest) -> APIResponse:
    """
    Primary endpoint for React Frontend -> AI Agent communication.
    Strictly isolated from business logic.
    """
    try:
        # Pass the validated Pydantic model directly to the Service Layer
        response = await ChatService.process_chat_message(request)
        
        # We still return HTTP 200 even if the agent caught a security violation
        # because the HTTP request itself was successful. The `success` boolean in 
        # the APIResponse dictates the application-level success.
        return response
        
    except Exception as e:
        logger.error(f"Critical routing error in /chat: {e}")
        # Only throw HTTP 500 if the Service Layer entirely collapses
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the request."
        )
