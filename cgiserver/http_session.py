"""HTTP Session.

Whenever a request comes from the server, a session will be created
based on the request, and a thread will be opened to run the session.
"""
from ensurepip import version
from inspect import stack
import socket
import logging
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
        self.logger = logging.getLogger()

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
        self._log_current_request(config, self.client_address, 200)
        
        self.client_socket.send(response)
        self.client_socket.close()

    def run(self, *args: Any, **kwds: Any) -> Any:
        """Run the session, handle an HTTP connection once"""
        # pylint: disable = unnecessary-dunder-call
        return self.__call__(args, kwds)
    
    def _log_current_request(self, config, client_address, status_code)->None:
        client_ip = client_address[0]
        client_port = client_address[1]
        method = config.method
        url = config.url
        http_version = config["http-version"]
        user_agent = config.headers["User-Agent"]
        content_length = config.headers["Content-Length"]

        text = f"[{client_ip}:{client_port}] \"{method} {url} {http_version}\" {status_code} {content_length} \"{user_agent}\""
        self.logger.info(text)
    
