"""HTTP Parser"""
from typing import Union
from utils import AttrDict, SplitQueue
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

        # TODO: Supports error and exception handling
        while not self.completed and not self.queue.empty:
            if not self.__parse_startline_done:
                self._parse_startline()
            if not self.__parse_headers_done and self.__parse_startline_done:
                self._parse_headers()
            if not self.__parse_content_done and self.__parse_headers_done:
                self._parse_content()

        return self.config if self.completed else None

    def _parse_startline(self) -> None:
        """Parse the first line of the http request"""
        startline = self.queue.pop("\r\n")
        # TODO: Resolve url to path, query string, fragment
        method, url, httpver = startline.split()
        self.config.update({"method": method, "url": url, "http-version": httpver})
        self.__parse_startline_done = True

    def _parse_headers(self) -> None:
        """Parse the headers of the http request"""
        while not self.queue.empty:
            headerline = self.queue.pop("\r\n")
            if headerline:
                name, value = headerline.strip().split(": ", 1)
                self.headers[name.upper()] = value
            else:
                self.__parse_headers_done = True
                break

        if "CONTENT-LENGTH" in self.headers:
            self.headers["CONTENT-LENGTH"] = int(self.headers["CONTENT-LENGTH"])
        else:
            self.headers["CONTENT-LENGTH"] = 0

    def _parse_content(self) -> None:
        """Parse the content of the http request"""
        content_length = self.headers["CONTENT-LENGTH"]
        if not self.queue.empty:
            self.config.content += self.queue.data
            self.queue.clear()
        if len(self.config.content) == content_length:
            self.__parse_content_done = True


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
