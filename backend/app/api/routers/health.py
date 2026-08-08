from fastapi import APIRouter, status
from datetime import datetime
from app.config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Monitoring"]
)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="System Health Check",
    description="Returns the status of the API, Database, and LLM Provider configuration."
)
async def get_health():
    """
    Useful for deployment monitoring and React frontend initial connectivity checks.
    """
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "configuration": {
            "llm_provider": settings.DEFAULT_LLM_PROVIDER,
            "database_url": settings.DATABASE_URL
        }
    }
