"""HTTP Server"""
import socket
from concurrent import futures
from typing import Any
from cgiserver.http_session import Session
from cgiserver.logging import get_logger

logger = get_logger()
MAX_CONN = 20


class HTTPServer:
    """A simple HTTP Server.

    Usage:
    >>> server = HTTPServer("127.0.0.1", 5500)
    >>> server.serve_forever()
    """

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def serve_forever(self) -> None:
        """Start the server, and whenever a new connection comes,
        create a session process to process the connection.
        """
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        # set timeout to catch socket.timeout exception
        # while being able to catch KeyboardInterrupt to stop server
        # see details: https://stackoverflow.com/questions/34871191/cant-close-socket-on-keyboardinterrupt
        server_socket.settimeout(1)
        logger.info("server running on http://%s:%s", self.host, self.port)
        executor = futures.ThreadPoolExecutor(MAX_CONN)
        while True:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                logger.info("server has been shutdown!")
                break
            executor.submit(Session(client_socket, client_address))
        executor.shutdown(wait=True)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.serve_forever()
