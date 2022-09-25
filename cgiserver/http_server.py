"""HTTP Server"""
import socket
from concurrent import futures
from typing import Any
from cgiserver.http_session import Session
from cgiserver.logging import get_logger
from cgiserver.setting import GLOBAL_SETTING

LOGGER = get_logger()


class HTTPServer:
    """A simple HTTP Server.

    Usage:
    >>> server = HTTPServer("127.0.0.1", 8888)
    >>> server.serve_forever()
    """

    def __init__(self, host: str, port: int, max_connection: int = 20) -> None:
        self.host = host
        self.port = port
        self.max_connection = max_connection
        self.should_stop = False

    def close(self) -> None:
        """close the server"""
        self.should_stop = True

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
        LOGGER.info("server running on http://%s:%s", self.host, self.port)
        GLOBAL_SETTING.check_setting("template_400")
        GLOBAL_SETTING.check_setting("template_403")
        GLOBAL_SETTING.check_setting("template_404")
        executor = futures.ThreadPoolExecutor(self.max_connection)
        while not self.should_stop:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break
            executor.submit(Session(client_socket, client_address))
        executor.shutdown(wait=True)
        LOGGER.info("server has been shutdown!")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.serve_forever()
