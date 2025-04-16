from logging.config import dictConfig
import logging
from .log_config import LogConfig

log_config = LogConfig().dict()
dictConfig(log_config)

logger = logging.getLogger("Project Template API")
logger.info(f"Logger initialized with parameters: {log_config}")