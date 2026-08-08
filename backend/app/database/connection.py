from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from app.config.settings import settings
import os

def get_db_connection() -> SQLDatabase:
    """
    Initializes and returns a LangChain SQLDatabase instance.
    This wrapper provides native schema introspection tools for the LLM.
    """
    # Ensure the data directory exists for SQLite
    if settings.DATABASE_URL.startswith("sqlite:///"):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Create SQLAlchemy engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Wrap in LangChain's SQLDatabase
    # We can explicitly include/exclude tables here if needed for security
    db = SQLDatabase(engine)
    
    return db

# Singleton instance for application use
db_instance = get_db_connection()
