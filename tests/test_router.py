import pytest
from cgiserver.router import Router, Route
from cgiserver.utils.exceptions import *


def test_router():
    router = Router()

    def callback1():
        pass

    def callback2():
        pass

    def callback3():
        pass

    def callback4():
        pass

    router.add("/webroot", method="GET", route=Route("/webroot", "GET", callback1))
    router.add("/webroot/a", method="POST", route=Route("/webroot/a", "GET", callback2))
    router.add("/webroot/b", method="HEAD", route=Route("/webroot/b", "GET", callback3))
    router.add(
        "/webroot/a/c", method="GET", route=Route("/webroot/a/c", "GET", callback4)
    )

    assert router.match("/webroot", "GET").callback is callback1
    assert router.match("/webroot/a", "POST").callback is callback2
    assert router.match("/webroot/b", "HEAD").callback is callback3
    assert router.match("/webroot/a/c", "GET").callback is callback4

    with pytest.raises(InvalidRoutePath):
        router.match("/webroot/d", "GET")
    with pytest.raises(InvalidRouteMethod):
        router.match("/webroot/a/c", "POST")
