"""HTML template loader"""
from typing import Union
from pathlib import Path


def html_file_loader(filename: Union[str, Path]) -> bytes:
    """Read a html file and encode it to a bytes.

    Args:
        filename (Union[str, Path]): file path.

    Raises:
        TypeError: filename is not an instance of str or Path.

    Returns:
        bytes: encoded str.
    """
    if not isinstance(filename, (str, Path)):
        raise TypeError(f"except str or Path type, get {type(filename)}")
    if isinstance(filename, str):
        filename = Path(filename)

    with open(filename, mode="r", encoding="utf-8") as file:
        return file.read().encode()
