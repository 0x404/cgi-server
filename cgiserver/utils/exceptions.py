"""Customer Exceptions"""


class RouteOverwriteError(Exception):
    """Reset an existing Route"""


class InvalidRoutePath(Exception):
    """Invalid route path"""


class InvalidRouteMethod(Exception):
    """Invalid route method"""


class RequestForbidden(Exception):
    """Request forbidden"""


class HTTPRequestError(Exception):
    """General HTTP request error"""


class InvalidMethod(HTTPRequestError):
    """Invalid HTTP method"""


class InvalidHeader(HTTPRequestError):
    """Invalid HTTP header"""


class InvalidContent(HTTPRequestError):
    """Invalid HTTP Content"""
