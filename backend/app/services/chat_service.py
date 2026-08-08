import logging
from app.agent.sql_agent import execute_agent_workflow
from app.schemas.chat import ChatRequest
from app.schemas.response import APIResponse

logger = logging.getLogger(__name__)

class ChatService:
    """
    Service Layer for handling chat operations.
    This entirely decouples the LangChain AI logic from the FastAPI routing logic.
    """
    
    @staticmethod
    async def process_chat_message(request: ChatRequest) -> APIResponse:
        """
        Receives a validated ChatRequest, executes the LangChain AI workflow,
        and returns a standardized APIResponse.
        """
        try:
            logger.info(f"Processing chat request for session: {request.session_id}")
            
            # The LCEL Agent Orchestrator is synchronous, so we run it directly here.
            # In a truly massive async application, we could run this in a ThreadPoolExecutor.
            agent_result = execute_agent_workflow(request.message)
            
            # The agent_result is a dict formatted by the PydanticOutputParser
            status = agent_result.get("status", "unknown")
            
            if status == "success" or status == "partial_success":
                return APIResponse(
                    success=True,
                    message="Query executed successfully.",
                    data=agent_result
                )
            else:
                # Catch cases where the agent caught a security violation or error
                return APIResponse(
                    success=False,
                    message="The agent encountered an error processing the request.",
                    error=agent_result
                )
                
        except Exception as e:
            logger.error(f"Unexpected error in ChatService: {e}")
            return APIResponse(
                success=False,
                message="An internal server error occurred while processing the chat.",
                error=str(e)
            )
