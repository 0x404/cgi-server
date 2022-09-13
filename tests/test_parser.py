from cgiserver.http_parser import HttpRequestParser


def test_parse_request():
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
    parse_result1 = parser.parse(HTTP_REQUEST1)
    parse_result2 = parser.parse(HTTP_REQUEST2)
    config = {
        "headers": {
            "Host": "127.0.0.1:8888",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Content-Length": 0,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6",
        },
        "content": "",
        "http-version": "HTTP/1.1",
        "method": "GET",
        "url": "/",
        "fragment": "",
        "query_string": {},
    }
    assert parse_result1 is None
    assert parse_result2 == config
