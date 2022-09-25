"""cgi server utils"""
from .attrdict import AttrDict
from .queue import SplitQueue
from .status import HTTPStatus
from .loader import html_file_loader

DEFAULT_HEADERS = AttrDict(
    {
        "User-Agent": "cgiserver/1.3.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }
)

__all__ = [
    "AttrDict",
    "SplitQueue",
    "HTTPStatus",
    "html_file_loader",
    "DEFAULT_HEADERS",
]
