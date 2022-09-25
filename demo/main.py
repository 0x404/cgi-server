from cgiserver import route, run
from cgiserver import GLOBAL_SETTING
from cgiserver.utils import html_file_loader


GLOBAL_SETTING.template_404 = "./static/404.html"


@route("/", method="GET")
def hello():
    return "this is index.html"


@route("/log", method="GET")
def log_page():
    return html_file_loader("logs/server_log.html")


@route("/cgi-bin/calculator.py", method="POST")
def calculate(**args):
    value1 = args.get("value1")
    value2 = args.get("value2")
    op = args.get("op")

    if any(arg is None for arg in (value1, value2, op)):
        return "argument error"

    try:
        value1 = float(value1)
        value2 = float(value2)
    except Exception:
        return "value1 or value2 is not a float or integer"

    if op == "+":
        return value1 + value2
    if op == "-":
        return value1 - value2
    if op == "*":
        return value1 * value2
    if op == "/":
        return value1 / value2

    return f"operation {op} not yet supported"


@route("/cgi-bin/query.py", method="POST")
def query(**args):
    student_id = args.get("id")
    if student_id is None:
        return "student id is None"
    # TODO


if __name__ == "__main__":
    run()
