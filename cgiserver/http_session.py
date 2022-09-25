"""HTTP Session.

Whenever a request comes from the server, a session will be created
based on the request, and a thread will be opened to run the session.
"""
import socket
from typing import Any
from cgiserver.logging import get_logger
from cgiserver.router import GLOBALROUTER
from cgiserver.utils import html_file_loader, AttrDict
from cgiserver.http_parser import HttpRequestParser, HttpResponseParser
from cgiserver.utils.exceptions import *

# pylint: disable = broad-except
try:
    NOFOUND_HTML = html_file_loader("cgiserver/static/404.html")
except Exception:
    NOFOUND_HTML = b"<p> 404 NO FOUND </p>"

BADREQUEST_HTML = html_file_loader("cgiserver/static/400.html")

LOGGER = get_logger()


class Session:
    """Used to handle an HTTP connection"""

    def __init__(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        self.client_socket = client_socket
        self.client_address = client_address

    def __call__(self, *args: Any, **kwds: Any) -> None:
        # parse client HTTP request
        # TODO: detect bad request and set status code to 400
        status_code = 0
        # try:
        parser = HttpRequestParser()
        data = self.client_socket.recv(1024)
        while (config := parser.parse(data)) is None:
            data = self.client_socket.recv(1024)

        # attempt to call the bound function to get the html body

        try:
            status_code = 200
            print("config.url, config.method", config.url, config.method)
            if parser.startlineMethodError is True:
                raise StartlineMethodError
            if parser.startlineURLError is True:
                raise StartlineURLError
            if parser.startlineHttpverError is True:
                raise StartlineHttpverError
            if parser.httpContentLengthError is True:
                raise HttpContentLengthError
            if parser.httpHeaderlineValueLoss is True:
                raise HttpHeaderlineValueLoss

            if len(str(config.url)) > 20:
                print("too long")
                raise UrlTooLong
            response_html = GLOBALROUTER.match(config.url, config.method)(
                **config.query_string
            )
            if not isinstance(response_html, (str, bytes)) and hasattr(
                    response_html, "__str__"
            ):
                response_html = str(response_html)
            if not isinstance(response_html, (str, bytes)) and not hasattr(
                    response_html, "__str__"
            ):
                response_html = (
                    f"<P> currently does not support {str(type(response_html))[1:-1]} "
                    f"as the return value of the decorated function</P>"
                )

        except (StartlineMethodError, StartlineURLError, StartlineHttpverError, HttpContentLengthError):
            print("400")
            status_code = 400
            response_html = BADREQUEST_HTML
        except UrlTooLong:
            print("Url too long")
            status_code = 400
            response_html = BADREQUEST_HTML
        except (RouteOverwriteError, InvalidRoutePath, InvalidRouteMethod):
            print("404")
            status_code = 404
            response_html = NOFOUND_HTML

        # response to client
        response = HttpResponseParser.make_response(
            status_code=status_code,
            headers=config.headers,
            body=response_html,
        )
        self._log_current_request(status_code, config)

        self.client_socket.send(response)
        self.client_socket.close()

    def run(self, *args: Any, **kwds: Any) -> None:
        """Run the session, handle an HTTP connection once"""
        # pylint: disable = unnecessary-dunder-call
        return self.__call__(args, kwds)

    def _log_current_request(self, status_code: int, config: AttrDict) -> None:
        """log current request.

        Args:
            config (AttrDict): HTTP request config.
            client_address (tuple[str, int]): client address.
            status_code (int): HTPP status code.
        """
        client_ip, client_port = self.client_address
        method = config.method
        url = config.url
        http_version = config.get("http-version", "HTTP/1.1")
        user_agent = config.headers["User-Agent"]
        content_length = config.headers["Content-Length"]

        msg = f'[{client_ip}:{client_port}] "{method} {url} {http_version}" {status_code} {content_length} "{user_agent}"'
        LOGGER.info(msg)
