"""HTTP Parser"""
import json
import urllib.parse as urlparse
from typing import Optional, Union
from cgiserver.utils import AttrDict, SplitQueue, HTTPStatus, DEFAULT_HEADERS
from cgiserver.utils.exceptions import (
    HTTPRequestError,
    InvalidMethod,
    InvalidHeader,
)

# pylint: disable = no-member


class HttpRequestParser:
    """Parse the HTTP request into a AttrDict conifg

    Usage:
    >>> parser = HttpRequestParser()
    >>> data = socket.recv(1024)
    >>> while (config := parser.parse(data)) is None:
    >>>     data = socket.recv(1024)
    """

    def __init__(self) -> None:
        self.config = AttrDict(headers=AttrDict(), content="")
        self.headers = self.config.headers
        self.queue = SplitQueue()
        self.__parse_startline_done = False
        self.__parse_headers_done = False
        self.__parse_content_done = False

    @property
    def completed(self) -> bool:
        """Whether the parsing is complete"""
        return self.__parse_content_done

    def parse(self, data: Union[str, bytes]) -> AttrDict:
        """Parse Http request.

        Args:
            data (Union[str, bytes]): http request.

        Returns:
            Optional[AttrDict]: a wraped python dict, include
            everything in this http request. return None if the parser
            is not completed.
        """
        if isinstance(data, bytes):
            data = data.decode("utf-8")

        self.queue.append(data)

        try:
            if not self.__parse_startline_done:
                self._parse_startline()
            if not self.__parse_headers_done and self.__parse_startline_done:
                self._parse_headers()
            if not self.__parse_content_done and self.__parse_headers_done:
                self._parse_content()
        except Exception as err:
            raise HTTPRequestError from err

        return self.config if self.completed else None

    def _parse_startline(self) -> None:
        """Parse the first line of the http request"""

        def _parse_query(query: str):
            """parse query string to key-value dict"""
            if len(query) == 0:
                return AttrDict()
            query = query.split("&")
            query = [item.split("=") for item in query]
            return AttrDict((item[0], item[1]) for item in query)

        startline = self.queue.pop("\r\n").strip()
        if len(startline.split()) != 3:
            raise HTTPRequestError
        method, url, httpver = startline.split()
        if method not in (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "TRACE",
            "CONNECT",
            "OPTIONS",
        ):
            raise InvalidMethod
        patrs = urlparse.urlsplit(url)
        self.config.update(
            {
                "http-version": httpver,
                "method": method,
                "url": patrs.path,
                "fragment": patrs.fragment,
                "query_string": _parse_query(patrs.query),
            }
        )
        self.__parse_startline_done = True

    def _parse_headers(self) -> None:
        """Parse the headers of the http request"""
        def headerline_interrupt_patch(queue: SplitQueue):
            """

            AsWeKnow header_line is \r\n(end flag) | ..*\r\n..*(header_content)

            assert queue & next_queue is header_line
            // TODO: bound condition would cause error
            discuss:
            have known queue, don't know next_queue.
            if queue.empty == false:
                assert queue is \r\n | ..*[!\r\n] | ..*\r\n.*
                exec line = queue.pop(delimiter=\r\n)
                if queue.empty:
                    assert queue is \r\n | ..*[!\r\n]
                    assert line is EMPTY | ..*
                    if line.empty:
                        assert line is end_flag.
                    else:
                        push ..*
                else: // queue not empty
                    assert queue is ..*\r\n.*
                    assert line is ..*
                    assert line is header_content.

            """

            line = queue.pop("\r\n")
            if line is None:
                return line

            if queue.empty and len(line) > 0:
                queue.append(line)
                return None

            return line


        while not self.queue.empty:
            headerline = headerline_interrupt_patch(self.queue)
            if headerline is None:
                break

            if headerline:
                if ":" not in headerline:
                    raise InvalidHeader
                name, value = headerline.strip().split(": ", 1)
                self.headers[name] = value
            else:
                self.__parse_headers_done = True
                break

        if "Content-Length" in self.headers:
            self.headers["Content-Length"] = int(self.headers["Content-Length"])
        else:
            self.headers["Content-Length"] = 0

    def _parse_content(self) -> None:
        """Parse the content of the http request"""
        content_length = self.headers["Content-Length"]
        if not self.queue.empty:
            self.config.content += self.queue.data
            self.queue.clear()
        if len(self.config.content) == content_length:
            if self.config.method == "POST":
                self.config.content = json.loads(self.config.content)
                self.config.query_string.update(self.config.content[0])
            self.__parse_content_done = True


class HttpResponseParser:
    """Parse Http Response"""

    @staticmethod
    def make_startline(status_code: int) -> bytes:
        """Make a HTTP startline.

        Args:
            status_code (int): status code.

        Returns:
            bytes: e.g. b"HTTP/1.1 200 OK\r\n"
        """
        # pylint: disable = no-value-for-parameter
        status_phrase = HTTPStatus(status_code).phrase
        status_code = str(status_code)
        return f"HTTP/1.1 {status_code} {status_phrase}\r\n".encode()

    @staticmethod
    def make_headers(headers: AttrDict) -> bytes:
        """Make a Http headers line.

        Args:
            headers (AttrDict): headers.

        Returns:
            bytes: e.g. b"Host: 127.0.0.1:8888\r\nConnection: keep-alive\r\n".
        """
        headerstr = "".join([f"{key}: {value}\r\n" for key, value in headers.items()])
        return headerstr.encode()

    @staticmethod
    def make_response(
        status_code: int,
        headers: Optional[AttrDict] = None,
        body: Union[str, bytes] = "",
    ):
        """make a HTTP response in bytes.

        Args:
            status_code (int): status code. e.g. 200, 404.
            headers (Optional[AttrDict], optional): html headers. Defaults to None.
            body (Union[str, bytes], optional): html body content. Defaults to "".

        Return:
            bytes: bytes ready to be sent.
        """
        headers = DEFAULT_HEADERS if headers is None else headers
        body = body.encode() if isinstance(body, str) else body

        if body:
            headers["Content-Length"] = len(body)
        else:
            headers.pop("Content-Length")

        content = [
            HttpResponseParser.make_startline(status_code),
            HttpResponseParser.make_headers(headers),
            b"\r\n",
            body,
        ]
        return b"".join(content)


if __name__ == "__main__":
    # pylint: disable = line-too-long
    HTTP_REQUEST1 = (
        b"GET / HTTP/1.1\r\n"
        b"Host: 127.0.0.1:8888\r\n"
        b"Connection: keep-alive\r\n"
        b"Cache-Control: max-age=0\r\n"
        b'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"\r\n'
        b"sec-ch-ua-mobile: ?0\r\n"
        b'sec-ch-ua-platform: "Windows"\r\n'
    )
    HTTP_REQUEST2 = (
        b"Upgrade-Insecure-Requests: 1\r\n"
        b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
        b"Sec-Fetch-Site: none\r\n"
        b"Sec-Fetch-Mode: navigate\r\n"
        b"Sec-Fetch-User: ?1\r\n"
        b"Sec-Fetch-Dest: document\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept-Language: en-GB,en;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6\r\n\r\n"
    )
    parser = HttpRequestParser()
    print(parser.parse(HTTP_REQUEST1))
    print(parser.parse(HTTP_REQUEST2))
