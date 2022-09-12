"""Customer Exceptions"""


class RouteOverwriteError(Exception):
    """Reset an existing Route"""


class InvalidRoutePath(Exception):
    """Invalid route path"""


class InvalidRouteMethod(Exception):
    """Invalid route method"""
