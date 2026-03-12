from core.logging.logger import logger


def test_logger_is_not_none():
    assert logger is not None


def test_logger_info_does_not_raise():
    logger.info("test_event", key="value")
