"""Router"""
from .router import Router, Route

ROUTER = Router()


def route(path, method="GET"):
    """A decorator to bind a function to a URL path.

    Args:
        path (str): request url path.
        method (str, optional): HTTP method, e.g. 'GET', 'POST'.
        Defaults to 'GET'.

    Usage:
    >>> @route('/webroot/index.html')
    >>> def index():
    >>>     response = html_file_loader("static/index.html")
    >>>     return response
    """

    def decorator(callback):
        new_route = Route(path, method, callback)
        ROUTER.add(path, method, new_route)
        return callback

    return decorator


__all__ = ["ROUTER", "Router", "Route", "route"]
