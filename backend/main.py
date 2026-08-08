import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import chat, health, database
from app.config.settings import settings
import uvicorn

# Configure centralized logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with OpenAPI metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise API linking a React UI to a LangChain SQL Database Agent.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# ---------------------------------------------------------
# CORS Configuration (Crucial for React Integration)
# ---------------------------------------------------------
# In production, specify exact domains. For development, we allow localhost.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Router Registration
# ---------------------------------------------------------
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(database.router, prefix=f"{settings.API_V1_STR}/database")

if __name__ == "__main__":
    logger.info("Starting AI SQL Database Agent Backend...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
