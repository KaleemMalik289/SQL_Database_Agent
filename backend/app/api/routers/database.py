from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, inspect
from app.config.settings import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/schema")
async def get_database_schema():
    """
    Introspects the database and returns a hierarchical JSON representation
    of all tables, their columns, data types, and primary keys.
    """
    try:
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        
        schema_data = []
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            primary_keys = inspector.get_pk_constraint(table_name).get('constrained_columns', [])
            
            column_data = []
            for col in columns:
                column_data.append({
                    "name": col["name"],
                    "type": str(col["type"]),
                    "is_primary_key": col["name"] in primary_keys,
                    "nullable": col.get("nullable", True)
                })
                
            schema_data.append({
                "table_name": table_name,
                "columns": column_data
            })
            
        return {
            "success": True,
            "data": schema_data
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch database schema: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve schema.")
