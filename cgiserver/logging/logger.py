"""logger"""
import os
import sys
import logging


def init_logger():
    """init root logger"""
    log_dir = os.environ.get("CGISERVER_LOGDIR", "./logs")
    html_log = os.path.join(log_dir, "server_log.html")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # set up root logger
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)

    general_formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] %(message)s")
    html_formatter = logging.Formatter(
        "<p>[%(asctime)s] - [%(levelname)s] %(message)s</p>"
    )
    html_handler = logging.FileHandler(
        html_log, mode="w+", encoding="utf-8", delay=False
    )
    console_handler = logging.StreamHandler(sys.stdout)

    html_handler.setFormatter(html_formatter)
    console_handler.setFormatter(general_formatter)

    logger.addHandler(html_handler)
    logger.addHandler(console_handler)


def get_logger(name: str = None):
    """Get logger.

    Args:
        name (str, optional): logger name. Defaults to None.

    Returns:
        Logger: logger with name.
    """
    return logging.getLogger(name)
