import socket
import threading
from cgiserver.http_server import HTTPServer


def test_server():
    HOST = "0.0.0.0"
    PORT = 5500
    server = HTTPServer(HOST, PORT)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    http_request = (
        b"GET / HTTP/1.1\r\n"
        b"Host: 0.0.0.0:5500\r\n"
        b"Connection: keep-alive\r\n"
        b"Cache-Control: max-age=0\r\n"
        b'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"\r\n'
        b"sec-ch-ua-mobile: ?0\r\n"
        b'sec-ch-ua-platform: "Windows"\r\n'
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
    client_socket.sendall(http_request)
    expected_response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Host: 0.0.0.0:5500\r\n"
        b"Connection: keep-alive\r\n"
        b"Cache-Control: max-age=0\r\n"
        b'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"\r\n'
        b"sec-ch-ua-mobile: ?0\r\n"
        b'sec-ch-ua-platform: "Windows"\r\n'
        b"Upgrade-Insecure-Requests: 1\r\n"
        b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
        b"Sec-Fetch-Site: none\r\n"
        b"Sec-Fetch-Mode: navigate\r\n"
        b"Sec-Fetch-User: ?1\r\n"
        b"Sec-Fetch-Dest: document\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept-Language: en-GB,en;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6\r\n"
        b"Content-Length: 617\r\n\r\n"
        b'<!doctype html>\n<html>\n\n<head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
        b'    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n'
        b"    <title>Error 404 - Page Not Found!</title>\n"
        b'    <link rel="stylesheet" type="text/css" href="http://mycgiserver.oss-cn-beijing.aliyuncs.com/css/style.css" />\n'
        b'</head>\n\n<body>\n    <div class="container">\n'
        b'        <img class="ops" src="http://mycgiserver.oss-cn-beijing.aliyuncs.com/images/404.svg" />\n'
        b"        <br />\n        <h3>There may be a problem with the path accessed.</h3>\n        <br />\n"
        b"    </div>\n</body>\n\n</html>"
    )
    http_response = client_socket.recv(4096)
    assert http_response == expected_response
    server.should_stop = True
