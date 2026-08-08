from langchain_core.tools import tool
from app.database.connection import db_instance
import re
import logging

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 1. Schema Inspection Tool
# -----------------------------------------------------------------------------
@tool
def get_database_schema() -> str:
    """
    Fetches the database schema, including table names, columns, and sample rows.
    Always call this tool first to understand the structure of the database before generating SQL.
    """
    try:
        schema_info = db_instance.get_table_info()
        logger.info("Successfully retrieved database schema.")
        return schema_info
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        return f"Error retrieving schema: {str(e)}"

# -----------------------------------------------------------------------------
# 2. SQL Validation Tool (Security Enforcement)
# -----------------------------------------------------------------------------
@tool
def validate_sql(query: str) -> dict:
    """
    Validates a generated SQL query to ensure it is strictly read-only.
    Rejects any query containing DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, CREATE, or PRAGMA.
    
    Args:
        query (str): The generated SQL query to validate.
        
    Returns:
        dict: {"is_valid": bool, "message": str, "query": str}
    """
    # Clean up formatting if the LLM wrapped it in markdown
    clean_query = query.strip()
    if clean_query.startswith("```sql"):
        clean_query = clean_query[6:]
    if clean_query.startswith("```"):
        clean_query = clean_query[3:]
    if clean_query.endswith("```"):
        clean_query = clean_query[:-3]
    clean_query = clean_query.strip()

    # List of dangerous SQL keywords
    dangerous_keywords = [
        r'\bDROP\b', r'\bDELETE\b', r'\bUPDATE\b', r'\bINSERT\b', 
        r'\bALTER\b', r'\bTRUNCATE\b', r'\bCREATE\b', r'\bPRAGMA\b',
        r'\bATTACH\b', r'\bDETACH\b'
    ]
    
    # Case-insensitive search for dangerous keywords
    query_upper = clean_query.upper()
    for pattern in dangerous_keywords:
        if re.search(pattern, query_upper):
            logger.warning(f"Security violation detected in query: {clean_query}")
            return {
                "is_valid": False, 
                "message": f"Security Violation: Query contains forbidden keyword matching pattern '{pattern}'. Only read-only operations are allowed.",
                "query": clean_query
            }
            
    if not query_upper.startswith("SELECT") and not query_upper.startswith("WITH"):
        logger.warning(f"Invalid query type (must start with SELECT or WITH): {clean_query}")
        return {
            "is_valid": False,
            "message": "Security Violation: Query must start with SELECT or WITH.",
            "query": clean_query
        }

    logger.info("SQL query passed validation.")
    return {
        "is_valid": True,
        "message": "Valid read-only query.",
        "query": clean_query
    }

# -----------------------------------------------------------------------------
# 3. SQL Execution Tool
# -----------------------------------------------------------------------------
@tool
def execute_sql(query: str) -> str:
    """
    Executes a securely validated SQL query against the database and returns the results.
    WARNING: The query MUST be validated using validate_sql before calling this tool.
    
    Args:
        query (str): The validated SQL query to execute.
        
    Returns:
        str: A stringified JSON representation of the query results.
    """
    try:
        logger.info(f"Executing SQL query: {query}")
        # db_instance.run automatically handles connection and limits results safely
        results = db_instance.run(query)
        return results
    except Exception as e:
        logger.error(f"SQL Execution Error: {e}")
        return f"SQL Execution Error: {str(e)}"
