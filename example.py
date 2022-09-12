"""Usage example:

Use the `route` decorator to decorate your custom function,
this will bind the function to the address corresponding to the URL.
Whenever a user visits the corresponding URL,
the system will call the function bound to the URL,
and pass the return value of the function to user through html.

So far, the return value of the decorated function should be a string.
In the next I will support more types like None, int, json etc.

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

from cgiserver import route, run


@route("/webroot", method="GET")
def web_page(**kwargs):
    """Bind function `web_page` to URL '/webroot'.

    Whenever a user visit `/webroot` using `GET` mehtod,
    he will get a `this is web root page` HTML page.
    """
    response = "<p> this is web root page </p>"
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

    Whenever a user visit `/webroot/index.html` using `GET` mehtod,
    he will get a `this is index page` HTML page.
    """
    response = "<p> this is index page </p>"
    return response


@route("/webroot/log")
def log_page(**kwargs):
    """This example is to tell you not to be limited to just a string,
    we can also open an html file and read it back,
    to achieve the effect of returning a html page.
    """
    try:
        with open("logs/server_log.html", mode="r", encoding="utf-8") as logfile:
            response = logfile.read()
    except FileNotFoundError:
        response = "<p> log file no found </p>"
    return response.encode()


if __name__ == "__main__":
    # When you have finished the definition of your website above
    # use the `run` function to run the server directly
    # and then you can browse your website through your browser
    run("127.0.0.1", 5500)
