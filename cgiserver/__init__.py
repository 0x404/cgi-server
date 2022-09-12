"""CGI Server"""
from .router import route
from .http_server import HTTPServer

__all__ = ["route", "HTTPServer"]


def run(host: str = "127.0.0.1", port: int = 5500):
    """wraped HTTPServer run.

    Args:
        host (str, optional): server host. Defaults to "127.0.0.1".
        port (int, optional): server port. Defaults to 5500.
    """
    server = HTTPServer(host, port)
    server.serve_forever()
