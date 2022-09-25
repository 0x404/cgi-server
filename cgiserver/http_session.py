"""HTTP Session.

Whenever a request comes from the server, a session will be created
based on the request, and a thread will be opened to run the session.
"""
import socket
from typing import Any, Union
from cgiserver.logging import get_logger
from cgiserver.router import GLOBALROUTER
from cgiserver.utils import AttrDict, DEFAULT_HEADERS
from cgiserver.http_parser import HttpRequestParser, HttpResponseParser
from cgiserver.setting import GLOBAL_SETTING
from cgiserver.utils.exceptions import (
    InvalidRoutePath,
    InvalidRouteMethod,
    RequestForbidden,
    HTTPRequestError,
)

# pylint: disable = broad-except
LOGGER = get_logger()


class Session:
    """Used to handle an HTTP connection"""

    def __init__(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        self.client_socket = client_socket
        self.client_address = client_address
        self.default_html = {
            400: GLOBAL_SETTING.template_400,
            403: GLOBAL_SETTING.template_403,
            404: GLOBAL_SETTING.template_404,
            200: "something went wrong",
        }

    def parser_http_request(self):
        """Parse HTTP request.

        Raises:
            HTTPRequestError: if got a bad http request.

        Returns:
            AttrDict: parse result.
        """
        parser = HttpRequestParser()
        data = self.client_socket.recv(1024)
        try:
            while (config := parser.parse(data)) is None:
                data = self.client_socket.recv(1024)
        except HTTPRequestError as err:
            raise HTTPRequestError from err
        return config

    def call_bound_function(self, config: AttrDict):
        """Attempt to call the bound function to get the html body

        Args:
            config (AttrDict): parser result.

        Returns:
            int: status code.
            Union[str, bytes]: response html body.
        """
        try:
            status_code = 200
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
        except (InvalidRoutePath, InvalidRouteMethod):
            status_code = 404
            response_html = self.default_html[status_code]
        except RequestForbidden:
            status_code = 403
            response_html = self.default_html[status_code]
        except Exception:
            status_code = 200
            response_html = self.default_html[status_code]
        return status_code, response_html

    def response_client(self, status_code: int, response_html: Union[str, bytes] = ""):
        """Send HTTP Response to clinet.

        Args:
            status_code (int): status code.
            response_html (Union[str, bytes], optional): response html body. Defaults to "".
        """
        response = HttpResponseParser.make_response(
            status_code=status_code,
            headers=DEFAULT_HEADERS,
            body=response_html,
        )
        self.client_socket.send(response)
        self.client_socket.close()

    def __call__(self, *args: Any, **kwds: Any) -> None:
        # step1: parse http request
        try:
            config = self.parser_http_request()
        except HTTPRequestError:
            self.response_client(400, self.default_html[400])
            return

        # step2: call bound function
        status_code, response_html = self.call_bound_function(config)

        # step3: response to clinet
        self.response_client(status_code, response_html)
        self._log_current_request(status_code, config)

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
