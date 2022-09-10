"""A wraped dict class"""
from typing import Any


class AttrDict(dict):
    """A wraped dict class, support accessw value through attributes.

    Usage:
    >>> d = AttrDict(a=1, b=2, c=3)
    >>> d
    {'a': 1, 'b': 2, 'c': 3}
    >>> d.a
    1
    >>> d['a']
    1
    >>> d.a = 3
    {'a': 3, 'b': 2, 'c': 3}
    """

    def __getattr__(self, __name: str) -> Any:
        try:
            return super().__getitem__(__name)
        except Exception as exception:
            raise KeyError(f"{__name} not in AttrDict") from exception

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, __value)
