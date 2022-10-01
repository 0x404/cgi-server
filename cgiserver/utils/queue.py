"""utils queue"""

from typing import Union


class SplitQueue:
    """A queue-like data structure that pops the
    first element before the separator each time

    Usage:
    >>> queue = SplitQueue(b'GET /index.html HTTP/1.1\r\nk1: v1; \r\nH2: k2: v2;\r\n')
    >>> while not que.empty:
    >>>     print(que.pop(b'\r\n'))
    b'GET /index.html HTTP/1.1'
    b'k1: v1; '
    b'H2: k2: v2;'
    """

    def __init__(self, data: Union[str, bytes] = "") -> None:
        self._data = data

    @property
    def empty(self) -> bool:
        """Whether this queue is empty"""
        return len(self._data) == 0

    @property
    def data(self) -> Union[str, bytes]:
        """Return a copy of this queue's data"""
        return self._data

    def clear(self) -> None:
        """Clear this queue"""
        self._data = ""

    def append(self, data: Union[str, bytes]) -> None:
        """append a data to the right of this queue"""
        self._data += data

    def pop(self, delimiter: Union[str, bytes]) -> Union[str, bytes]:
        """Pop the first element before the delimiter.

        Args:
            delimiter (Union[str, bytes]): delimiter to split the string.

        Raises:
            ValueError: pop if the queue is already empty.

        Returns:
            Union[str, bytes]: the first element before the delimiter.
        """
        if self.empty:
            raise ValueError("SplitQueue is empty")
        first, *rest = self._data.split(delimiter, 1)
        self._data = "" if not rest else rest[0]
        return first

    def pop_str_end_with(self, delimiter: Union[str, bytes]) -> Union[str, bytes]:
        """Pop the first element before the delimiter.

        Args:
            delimiter (Union[str, bytes]): delimiter to split the string.

        Raises:
            ValueError: pop if the queue is already empty.

        Returns:
            Union[str, bytes]: the first element end with the delimiter.
        """
        if self.empty:
            raise ValueError("SplitQueue is empty")
        first, *rest = self._data.split(delimiter, 1)
        if len(rest) == 0:
            return None

        self._data = "" if not rest else rest[0]
        return first
