"""logging"""
import os
import sys
import logging
from .logger import get_logger

LOGFILE_DIR = "./logs"
HTML_LOG_LOCATION = LOGFILE_DIR + "/server_log.html"

if not os.path.exists(LOGFILE_DIR):
    os.makedirs(LOGFILE_DIR, exist_ok=True)

__logger = logging.getLogger()  # get root logger
__logger.setLevel(level=logging.INFO)

__general_formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] %(message)s")
__html_formatter = logging.Formatter(
    "<p>[%(asctime)s] - [%(levelname)s] %(message)s</p>"
)
__html_handler = logging.FileHandler(
    HTML_LOG_LOCATION, mode="w+", encoding="utf-8", delay=False
)
__console_handler = logging.StreamHandler(sys.stdout)

__html_handler.setFormatter(__html_formatter)
__console_handler.setFormatter(__general_formatter)

__logger.addHandler(__html_handler)
__logger.addHandler(__console_handler)

__all__ = ["get_logger"]
