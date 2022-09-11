"""cgi server utils"""
from .attrdict import AttrDict
from .queue import SplitQueue
from .status import HTTPStatus
from .loader import html_file_loader

__all__ = ["AttrDict", "SplitQueue", "HTTPStatus", "html_file_loader"]
