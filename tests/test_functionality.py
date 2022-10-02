import threading
import socket
from time import sleep
from cgiserver import route
from cgiserver.http_server import HTTPServer


@route("/")
def index_page(**args):
    return "this is index page"


@route("/echo")
def echo_page_get(**args):
    return "this is echo page"


@route("/echo", method="POST")
def echo_page_post(**args):
    return args.get("user")


@route("/calculate", method="POST")
def calculate_page_post(**args):
    value1 = args.get("value1")
    value2 = args.get("value2")
    op = args.get("op")
    if any(arg is None for arg in (value1, value2, op)):
        return "argument error"

    try:
        value1 = int(value1)
        value2 = int(value2)
    except Exception:
        return f"value1 {value1} or value2 {value2} is not a integer"

    if op == "+":
        return value1 + value2
    if op == "-":
        return value1 - value2
    if op == "*":
        return value1 * value2
    if op == "/":
        return value1 / value2
    return f"op {op} currently not supported"


def test_functionality():
    HOST = "127.0.0.1"
    PORT = 6000
    stop_event = threading.Event()
    server = HTTPServer(HOST, PORT, stop_event=stop_event)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    sleep(1)

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    request1 = (
        b"GET / HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response1 = (
        b"HTTP/1.1 200 OK\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 18\r\n\r\n"
        b"this is index page"
    )
    client_socket.sendall(request1)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        stop_event.set()
        client_socket.sendall(request1)
        print("test_functionality: test case1 error")
        assert False
    assert response1 == http_response

    request2 = (
        b"POST /echo?user=test HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response2 = (
        b"HTTP/1.1 200 OK\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 4\r\n\r\n"
        b"test"
    )

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request2)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        stop_event.set()
        client_socket.sendall(request2)
        print("test_functionality: test case2 error")
        assert False
    assert response2 == http_response

    request3 = (
        b"POST /calculate?value1=10&value2=20&op=+ HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response3 = (
        b"HTTP/1.1 200 OK\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 2\r\n\r\n"
        b"30"
    )

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request3)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        stop_event.set()
        client_socket.sendall(request3)
        print("test_functionality: test case3 error")
        assert False
    assert response3 == http_response

    request4 = (
        b"POST /calculate?value1=10&value2=20&op=mod HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response4 = (
        b"HTTP/1.1 200 OK\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 30\r\n\r\n"
        b"op mod currently not supported"
    )

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request4)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        stop_event.set()
        client_socket.sendall(request4)
        print("test_functionality: test case4 error")
        assert False
    assert response4 == http_response
    stop_event.set()
