import logging
from langchain_core.runnables import RunnablePassthrough
from app.llm.provider_factory import get_llm
from app.agent.prompts import sql_generation_prompt, interpretation_prompt
from app.agent.output_parser import agent_response_parser
from app.tools.sql_tools import get_database_schema, validate_sql, execute_sql

logger = logging.getLogger(__name__)

def execute_agent_workflow(question: str) -> dict:
    """
    The core LCEL Orchestrator for the AI SQL Database Agent.
    Strictly follows the required flow:
    Intent -> Schema -> Generate SQL -> Validate -> Execute -> Analyze -> Explain
    """
    logger.info(f"Starting agent workflow for question: {question}")
    llm = get_llm()

    # ---------------------------------------------------------
    # STEP 1: Schema Inspection
    # ---------------------------------------------------------
    logger.info("Step 1: Inspecting Schema")
    schema_info = get_database_schema.invoke({})
    
    # ---------------------------------------------------------
    # STEP 2: Generate SQL (LCEL Chain 1)
    # ---------------------------------------------------------
    logger.info("Step 2: Generating SQL")
    # LCEL Pipeline: Prompt -> LLM -> String Output
    sql_generation_chain = sql_generation_prompt | llm 
    
    generation_response = sql_generation_chain.invoke({
        "question": question,
        "schema": schema_info
    })
    generated_sql = generation_response.content.strip()
    
    if generated_sql.startswith("CONVERSATION:"):
        response_text = generated_sql.replace("CONVERSATION:", "").strip()
        logger.info("Conversational intent detected.")
        return {
            "question": question,
            "generated_sql": "",
            "result": [],
            "summary": response_text,
            "status": "success"
        }
        
    if generated_sql.startswith("ERROR:"):
        logger.warning(f"SQL Generation aborted: {generated_sql}")
        return {
            "question": question,
            "generated_sql": "",
            "result": [],
            "summary": generated_sql,
            "status": "error"
        }

    # ---------------------------------------------------------
    # STEP 3 & 4: Validate and Execute SQL
    # ---------------------------------------------------------
    logger.info("Step 3: Validating SQL")
    validation = validate_sql.invoke(generated_sql)
    
    if not validation["is_valid"]:
        logger.error(f"Validation failed: {validation['message']}")
        return {
            "question": question,
            "generated_sql": validation["query"],
            "result": [],
            "summary": validation["message"],
            "status": "security_violation"
        }
        
    safe_sql = validation["query"]
    
    logger.info("Step 4: Executing SQL")
    raw_results = execute_sql.invoke(safe_sql)

    # ---------------------------------------------------------
    # STEP 5: Interpret Results (LCEL Chain 2)
    # ---------------------------------------------------------
    logger.info("Step 5: Generating Business Interpretation")
    # Inject format instructions into the prompt system dynamically
    # LCEL Pipeline: Prompt -> LLM -> PydanticOutputParser
    
    interpretation_chain = interpretation_prompt | llm | agent_response_parser
    
    try:
        final_response = interpretation_chain.invoke({
            "question": question,
            "sql_query": safe_sql,
            "results": raw_results,
            "format_instructions": agent_response_parser.get_format_instructions()
        })
        
        # Pydantic Output Parser returns a structured object, we convert to dict
        logger.info("Workflow completed successfully.")
        return final_response.model_dump()
        
    except Exception as e:
        logger.error(f"Error parsing final output: {e}")
        # Fallback raw response if parsing fails
        return {
            "question": question,
            "generated_sql": safe_sql,
            "result": raw_results,
            "summary": f"Failed to format response neatly. Raw result: {raw_results}",
            "status": "partial_success"
        }
