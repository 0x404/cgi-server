"""HTTP Server"""
import threading
import socket
import logging
from typing import Any
from cgiserver.http_session import Session


class HTTPServer:
    """A simple HTTP Server.

    Usage:
    >>> server = HTTPServer("127.0.0.1", 5500)
    >>> server.serve_forever()
    """

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.logger = self._setup_logger()

    def serve_forever(self) -> None:
        """Start the server, and whenever a new connection comes,
        create a session process to process the connection.
        """
        self.logger.info("server running...")
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        # set timeout to catch socket.timeout exception
        # while being able to catch KeyboardInterrupt to stop server
        # see details: https://stackoverflow.com/questions/34871191/cant-close-socket-on-keyboardinterrupt
        server_socket.settimeout(1)
        print(f"server running on http://{self.host}:{self.port}")
        while True:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break
            handle_thread = threading.Thread(
                target=Session(client_socket, client_address)
            )
            handle_thread.start()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.serve_forever()

    def __del__(self) -> None:
        logging.info("server has been shutdown!")

    def _setup_logger(self):
        logger = logging.getLogger()  # get root logger
        logger.setLevel(level=logging.INFO)

        file_formatter = logging.Formatter(
            "[%(asctime)s] - [%(levelname)s] %(message)s"
        )
        file_handler = logging.FileHandler(
            "./cgiserver/log/basic_log.log", mode="a+", encoding="utf-8", delay=False
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        html_formatter = logging.Formatter(
            "<p>[%(asctime)s] - [%(levelname)s] %(message)s</p>"
        )
        html_handler = logging.FileHandler(
            "./cgiserver/log/log.html", mode="a+", encoding="utf-8", delay=False
        )
        html_handler.setFormatter(html_formatter)
        logger.addHandler(html_handler)

        return logger


if __name__ == "__main__":
    server = HTTPServer("127.0.0.1", 5500)
    server.serve_forever()
