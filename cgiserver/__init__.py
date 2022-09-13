"""CGI Server"""
from argparse import ArgumentParser
from .router import route
from .http_server import HTTPServer


def run(host: str = "127.0.0.1", port: int = 8888, max_connection: int = 20):
    """wraped HTTPServer run.

    Args:
        host (str, optional): server host. Defaults to "127.0.0.1".
        port (int, optional): server port. Defaults to 5500.
    """
    server = HTTPServer(host, port, max_connection)
    server.serve_forever()


def crun():
    """wraped HTTPServer run, launch server from command line"""
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="server's host")
    parser.add_argument("--port", type=int, default=8888, help="server's port")
    parser.add_argument(
        "-m", "--maxconnect", type=int, default=20, help="max connections"
    )

    args = parser.parse_args()
    run(host=args.host, port=args.port, max_connection=args.maxconnect)


__all__ = ["route", "run", "crun"]
