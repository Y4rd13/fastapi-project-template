from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "Project Template API"
    LOG_FORMAT: str = "[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s"
    LOG_LEVEL: str = "INFO" # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Stream to stdout
        },
    }
    loggers: dict = {
    LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    "uvicorn": {"handlers": ["default"], "level": LOG_LEVEL},
    }