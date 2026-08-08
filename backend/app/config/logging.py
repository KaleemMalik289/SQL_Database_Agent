import logging
import sys
from .settings import settings

def setup_logging():
    """
    Configures centralized logging for the application.
    Outputs to stdout with a standard format.
    """
    log_level_name = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set specific log levels for noisy libraries if necessary
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(settings.PROJECT_NAME)
