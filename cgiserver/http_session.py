"""HTTP Session.

Whenever a request comes from the server, a session will be created
based on the request, and a thread will be opened to run the session.
"""
import socket
from typing import Any
from utils import html_file_loader
from http_parser import HttpRequestParser, HttpResponseParser


class Session:
    """Used to handle an HTTP connection"""

    def __init__(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        self.client_socket = client_socket
        self.client_address = client_address

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        parser = HttpRequestParser()
        data = self.client_socket.recv(1024)
        while (config := parser.parse(data)) is None:
            data = self.client_socket.recv(1024)

        # TODO: supprot CGI router here
        # pylint: disable=broad-except
        try:
            response_html = html_file_loader("static/404.html")
        except Exception:
            response_html = b"<p> 404 NO FOUND </p>"
        response = HttpResponseParser.make_response(200, config.headers, response_html)
        self.client_socket.send(response)
        self.client_socket.close()

    def run(self, *args: Any, **kwds: Any) -> Any:
        """Run the session, handle an HTTP connection once"""
        # pylint: disable = unnecessary-dunder-call
        return self.__call__(args, kwds)
