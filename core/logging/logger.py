import structlog
import logging


logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)

logger = structlog.get_logger()
