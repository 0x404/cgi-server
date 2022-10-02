import socket
import threading
from time import sleep
from cgiserver.http_server import HTTPServer


def test_server():

    HOST = "127.0.0.1"
    PORT = 5500
    stop_event = threading.Event()
    server = HTTPServer(HOST, PORT, stop_event=stop_event)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    sleep(1)

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
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 18\r\n\r\n"
        b"this is index page"
    )
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        client_socket.sendall(http_request)
        stop_event.set()
        server_thread.join()
        assert False
    if http_response != expected_response:
        stop_event.set()
    assert http_response == expected_response
    stop_event.set()
    # client_socket.sendall(http_request)
