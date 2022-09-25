"""Customer Exceptions"""


class RouteOverwriteError(Exception):
    """Reset an existing Route"""


class InvalidRoutePath(Exception):
    """Invalid route path"""


class InvalidRouteMethod(Exception):
    """Invalid route method"""


class UrlTooLong(Exception):
    """Url too long"""


class StartlineMethodError(Exception):
    """StartlineMethodError"""


class StartlineURLError(Exception):
    """StartlineURLError"""


class StartlineHttpverError(Exception):
    """StartlineHttpverError"""


class HttpContentLengthError(Exception):
    """HttpContentLengthError"""


class HttpHeaderlineValueLoss(Exception):
    """HttpHeaderlineValueLoss"""


class TimeOutError(Exception):
    """TimeOutError"""
