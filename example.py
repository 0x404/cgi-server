"""Usage example:

Use the `route` decorator to decorate your custom function,
this will bind the function to the address corresponding to the URL.
Whenever a user visits the corresponding URL,
the system will call the function bound to the URL,
and pass the return value of the function to user through html.

At the current position, the return value of the decorated function can be any type,
such as `str`, `bytes`, `int`, `float`, or even `None`.
It can also be a custom type, but in order to enable the custom type to be transmitted through html,
please implement `__str__` method for the custom type.

In the future I would like to support the following feature,
I think this feature is more user-friendly,
we don't need to find the parameters we want from **kwargs.

    @route("/webroot/calculator?<int><int><str>", method="POST")
    def calculate(value1, value2, op):
        if op == "+":
            ans = value1 + value2
        elif op == "-":
            ans = value1 - value2
        elif op == "*":
            ans = value1 * value2
        elif op == "/":
            ans = value1 / value2
        return value

To pass the query string of the URL to the parameter of the binding function,
and convert it to the corresponding type, I think it's not easy and a lot of effort is needed.
"""
import json
from cgiserver import route, run, crun


@route("/webroot", method="GET")
def web_page(**kwargs):
    """Bind function `web_page` to URL '/webroot'.

    Whenever a user visit `/webroot` using `GET` mehtod,
    he will get a `this is web root page` HTML page.
    """

    with open("root.html", mode="r", encoding="utf-8") as logfile:
        response = logfile.read()
    # response = "<p> this is web root page </p>"
    return response


@route("/webroot/echo", method="POST")
def echo(**kwargs):
    """Bind function `echo` to URL '/webroot/echo'.

    Whenever a user visit `/webroot/echo` using `POST` mehtod,
    The system will call this echo function and pass the parameters of the URL to `**kwargs`.

    The return value of this function will send to user through HTML page.
    With this approach, we implement dynamic pages.
    """
    user = kwargs.get("user", "none")
    response = f"<p> hello {user}, welcome to echo page. </p>"
    return response


@route("/webroot/index.html")
def index_page(**kwargs):
    """Decorator's method argument defaults to `GET`.

    You can not only return an HTML string, but also a Json string.

    Whenever a user visit `/webroot/index.html` using `GET` mehtod,
    he will get a Json objcet with key `content` and `query`.
    """
    response = {"content": "this is index.html", "query": kwargs}
    return json.dumps(response)


@route("/webroot/log")
def log_page(**kwargs):
    """This example is to show you not to be limited to just a string,
    we can also open an html file and read it back,
    to achieve the effect of returning a html page.
    """
    try:
        with open("logs/server_log.html", mode="r", encoding="utf-8") as logfile:
            response = logfile.read()
    except FileNotFoundError:
        response = "<p> log file no found </p>"
    return response.encode()


@route("/calculate", method="GET")
def calculate(**kwargs):
    try:
        with open("calculate.html", mode="r", encoding="utf-8") as logfile:
            response = logfile.read()
    except FileNotFoundError:
        response = "<p> calculate file no found </p>"
    return response


@route("/cal_ans", method="POST")
def cal_ans(**kwargs):
    try:
        with open("calculate.html", mode="r", encoding="utf-8") as file:
            response = file.read()
    except FileNotFoundError:
        response = "<p> file no found </p>"
    return response


@route("/dataquery", method="GET")
def dataquery(**kwargs):
    try:
        with open("DataQuery.html", mode="r", encoding="utf-8") as logfile:
            response = logfile.read()
    except FileNotFoundError:
        response = "<p> calculate file no found </p>"
    return response


if __name__ == "__main__":
    # When you have finished the definition of your website above,
    # use the function `run` to run the server directly,
    # and then you can browse your website through your browser.

    run("127.0.0.1", 8888)

    # You can also launch the server via the command line,
    # Use the function `crun` and give the corresponding parameters on the command line.
    # e.g. python examply.py --host "127.0.0.1" --port 8888 --maxconnect 20

    # crun()
