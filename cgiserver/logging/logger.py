"""logger"""
import logging


def get_logger(name: str = None):
    """Get logger.

    Args:
        name (str, optional): logger name. Defaults to None.

    Returns:
        Logger: logger with name.
    """
    return logging.getLogger(name)
