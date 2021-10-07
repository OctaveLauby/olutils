"""Convenient way to build quick overview of long containers"""
from typing import Any, Iterable, List


def lazy_content(__list: List, /, nvals: int, ellipsis: Any = ...) -> List:
    """Return list at most {nvals} items from object

    Extra values are replaced with mid_value

    Examples:
        >>> lazy_content([1, 2, 3, 4, 5], 3)
        ... [1, ..., 5]
    """
    if len(__list) <= nvals:
        return __list
    return (
        __list[: nvals // 2] + [ellipsis] + __list[len(__list) - abs(nvals - 1) // 2 :]
    )


class LazyList:
    """List with lazy representation"""

    def __init__(self, iterable: Iterable, /, nvals: int, ellipsis: Any = ...):
        """Initialize instance

        Args:
            iterable    : iterable on content
            nvals       : max number of objects to display in str/repr
            ellipsis    : object used to replace hidden values
        """
        self._content: List = list(iterable)
        self.nvals: int = nvals
        self.ellipsis: Any = ellipsis

    @property
    def content(self) -> List:
        """Full content as list"""
        return self._content

    @property
    def lazycontent(self) -> List:
        """Lazy content list"""
        return lazy_content(
            self.content,
            nvals=self.nvals,
            ellipsis=self.ellipsis,
        )

    def append(self, __obj: Any, /):
        """Append object to the end of the list"""
        return self.content.append(__obj)

    def insert(self, __index: int, __obj: Any, /):
        """Insert object before index"""
        return self.content.insert(__index, __obj)

    def __len__(self) -> int:
        return len(self.content)

    def __repr__(self) -> str:
        return repr(self.lazycontent)

    def __str__(self) -> str:
        return str(self.lazycontent)
