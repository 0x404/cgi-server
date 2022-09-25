"""Router: mapping URL:method to a callable object"""
# pylint: disable = wildcard-import
from typing import Any
from cgiserver.utils.exceptions import (
    RouteOverwriteError,
    InvalidRouteMethod,
    InvalidRoutePath,
)


class Route:
    """A Route corresponds to a Callable object"""

    def __init__(self, path, method, callback) -> None:
        self.path = path
        self.method = method
        self.callback = callback

    def undecorate_callback(self):
        """Get origin function signature to improve the use of POST"""
        # TODO: get origin function signature

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.callback(*args, **kwds)


class TreeNode:
    """Organize URLs into a tree"""

    def __init__(self, name: str, route: Route = None) -> None:
        self.name = name
        self.method2route = {}
        self.sub_nodes = {}
        if route is not None:
            self.add_route(route.method, route)

    def has_route(self, method: str) -> bool:
        """Whether there is a route bound with `method`.

        Args:
            method (str): HTTP method (`GET`, `POST`, ...).

        Returns:
            bool: Whether there is a route bound with `method`.
        """
        return method in self.method2route

    def add_route(self, method: str, route: Route) -> None:
        """Add a route to current tree node.

        Args:
            method (str): HTTP method (`GET`, `POST`, ...).
            route (Route): Route object to be bound.

        Raises:
            RouteOverwriteError: Route already exists.
        """
        if method in self.method2route:
            raise RouteOverwriteError
        self.method2route[method] = route

    def get_route(self, method: str) -> Route:
        """Get route object by method.

        Args:
            method (str): HTTP method (`GET`, `POST`, ...).

        Returns:
            Route: required route object.
        """
        return self.method2route[method]

    def has_child(self, child_name: str) -> bool:
        """Whether there is a child tree node called `child_name`.

        Args:
            child_name (str): child node name.

        Returns:
            bool: Whether there is a child tree node called `child_name`.
        """
        return child_name in self.sub_nodes

    def add_child(self, child_node) -> None:
        """Add a child tree node to current node.

        Args:
            child_node (TreeNode): child tree node to be added.
        """
        self.sub_nodes[child_node.name] = child_node

    def get_child(self, child_name: str):
        """Get child node by name.

        Args:
            child_name (str): child node name.

        Returns:
            TreeNode: child node.
        """
        return self.sub_nodes[child_name]

    def __repr__(self) -> str:
        """For debug"""
        return f"{self.name}'s nodes: {self.sub_nodes.keys()}\n"


class Router:
    """Router: manage the mapping from URLs to callable objects"""

    def __init__(self) -> None:
        self.paths = []
        self.root = TreeNode("/")

    def _itertokens(self, path: str):
        """Generate tokens in a valid path.

        Args:
            path (str): a route path. e.g. "/cgi_bin/hello.py"
        """
        # TODO: support regular matching
        # the current method is too weak
        path = path.strip("/")
        tokens = path.split("/")
        for token in tokens:
            yield token

    def add(self, path: str, method: str, route: Route):
        """Add a route to this Router.

        Args:
            path (str): URL path.
            method (str): HTTP method (`GET`, `POST`, ...).
            route (Route): `Route` object.
        """
        current_node = self.root
        for token in self._itertokens(path):
            if not current_node.has_child(token):
                current_node.add_child(TreeNode(token))
            current_node = current_node.sub_nodes[token]
        try:
            current_node.add_route(method, route)
        except RouteOverwriteError:
            print("disable rewriting of existing routes")

    def match(self, path: str, method: str):
        """match a (URL, method) pair.

        Args:
            path (str): URL path.
            method (str): HTTP method (`GET`, `POST`, ...).

        Raises:
            InvalidRoutePath: URL path is invalid.
            InvalidRouteMethod: does not have an associated route with method.

        Returns:
            Route: matched route object.
        """
        # self._debug(self.root)
        current_node = self.root
        for token in self._itertokens(path):
            if not current_node.has_child(token):
                raise InvalidRoutePath
            current_node = current_node.get_child(token)

        if not current_node.has_route(method):
            raise InvalidRouteMethod
        return current_node.get_route(method)

    def _debug(self, node: TreeNode):
        """just for debug"""
        print(node)
        for _, next_node in node.sub_nodes.items():
            self._debug(next_node)
