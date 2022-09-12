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
        self.logger.info("server starting...")
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


    def _setup_logger(self):
        logger = logging.getLogger()  # get root logger
        handler = logging.FileHandler("./cgiserver/log/log.log",mode='a+', encoding='utf-8', delay=False)
        formatter = logging.Formatter(
            '[%(asctime)s] - [%(levelname)s] %(message)s')  # 规定输出格式
        handler.setFormatter(formatter)  # 将输出格式指定到handler上
        logger.addHandler(handler)
        logger.setLevel(level=logging.INFO)
        return logger



if __name__ == "__main__":
    server = HTTPServer("127.0.0.1", 5500)
    server.serve_forever()
