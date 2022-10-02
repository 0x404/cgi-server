import threading
import socket
import pytest
from time import sleep
from cgiserver import route
from cgiserver.http_server import HTTPServer
from cgiserver.router import GLOBALROUTER

HOST = "127.0.0.1"
PORT = 6000


@pytest.fixture
def setup_nofound():
    GLOBALROUTER.cleanup()
    yield None
    GLOBALROUTER.cleanup()


@pytest.fixture
def setup_server():
    stop_event = threading.Event()
    server = HTTPServer(HOST, PORT, stop_event=stop_event)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    sleep(1)
    yield server
    stop_event.set()
    server_thread.join()
    sleep(2)


@pytest.fixture
def setup_root():
    GLOBALROUTER.cleanup()

    @route("/")
    def index_page(**args):
        return "this is index page"

    yield None
    GLOBALROUTER.cleanup()


@pytest.fixture
def setup_echo():
    GLOBALROUTER.cleanup()

    @route("/echo", method="POST")
    def echo_page_post(**args):
        return args.get("user")

    yield None
    GLOBALROUTER.cleanup()


@pytest.fixture
def setup_calculate():
    GLOBALROUTER.cleanup()

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

    yield None
    GLOBALROUTER.cleanup()


def test_nofound(setup_nofound, setup_server):
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
    expected_response = (
        b"HTTP/1.1 404 Not Found\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 29\r\n\r\n"
        b"Nothing matches the given URI"
    )
    client_socket.sendall(http_request)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        assert False
    assert http_response == expected_response


def test_root(setup_root, setup_server):
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    request = (
        b"GET / HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"User-Agent: cgiserver/1.3.0\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Accept: */*\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 18\r\n\r\n"
        b"this is index page"
    )
    client_socket.sendall(request)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        assert False
    assert http_response == response


def test_echo(setup_echo, setup_server):
    request = (
        b"POST /echo?user=test HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response = (
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
    client_socket.sendall(request)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        assert False
    assert http_response == response


def test_calculate(setup_calculate, setup_server):
    request = (
        b"POST /calculate?value1=10&value2=20&op=+ HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response = (
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
    client_socket.sendall(request)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        assert False
    assert http_response == response

    request = (
        b"POST /calculate?value1=10&value2=20&op=mod HTTP/1.1\r\n"
        b"Host: 127.0.0.1:1234\r\n"
        b"User-Agent: pytest/1.0.0\r\n"
        b"Accept: */*\r\n"
        b"Accept-Encoding: gzip, deflate, br\r\n"
        b"Connection: keep-alive\r\n\r\n"
    )
    response = (
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
    client_socket.sendall(request)
    client_socket.settimeout(5)
    try:
        http_response = client_socket.recv(4096)
    except socket.timeout:
        assert False
    assert http_response == response
