"""CGI Server"""
import os
from argparse import ArgumentParser
from .router import route
from .http_server import HTTPServer
from .logging import init_logger
from .setting import GLOBAL_SETTING


def run(
    host: str = "127.0.0.1",
    port: int = 8888,
    max_connection: int = 20,
    log_dir: str = None,
):
    """wraped HTTPServer run.

    Args:
        host (str, optional): server host. Defaults to "127.0.0.1".
        port (int, optional): server port. Defaults to 5500.
        max_connection (int, optional): maximum thread num in server thread pool. Defaults to 20.
        log_dir (str, optional): directory of log file. Defaults to `pwd/logs`
    """
    if log_dir is not None:
        os.environ["CGISERVER_LOGDIR"] = log_dir
    init_logger()
    server = HTTPServer(host, port, max_connection)
    server.serve_forever()


def crun():
    """wraped HTTPServer run, launch server from command line"""
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="server's host")
    parser.add_argument("--port", type=int, default=8888, help="server's port")
    parser.add_argument("-m", "--maxc", type=int, default=20, help="max connections")
    parser.add_argument("-l", "--logdir", type=str, default=None, help="log dir")

    args = parser.parse_args()
    run(host=args.host, port=args.port, max_connection=args.maxc, log_dir=args.logdir)


__all__ = ["route", "run", "crun", "GLOBAL_SETTING"]
