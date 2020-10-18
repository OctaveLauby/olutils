"""Convenient way to build quick overview of long containers"""


def lazy_content(__object, nvals, ellipsis=...):
    """Return list at most {nvals} items from object

    Extra values are replaced with mid_value


    Examples:
        >>> lazy_content([1, 2, 3, 4, 5], 3)
        ... [1, ..., 5]
    """
    if len(__object) <= nvals:
        return __object
    return (
            __object[:nvals // 2]
            + [ellipsis]
            + __object[len(__object) - abs(nvals - 1) // 2:]
    )


class LazyList:
    """List with lazy representation"""

    def __init__(self, __object, nvals, ellipsis=...):
        self._content = list(__object)
        self.nvals = nvals
        self.ellipsis = ellipsis

    @property
    def content(self):
        """Full content"""
        return self._content

    @property
    def lazycontent(self):
        """Lazy content list"""
        return lazy_content(
            self.content,
            nvals=self.nvals,
            ellipsis=self.ellipsis,
        )

    def append(self, __object):
        """Append object to the end of the list"""
        return self.content.append(__object)

    def insert(self, __index, __object):
        """Insert object before index"""
        return self.content.insert(__index, __object)

    def __len__(self):
        return len(self.content)

    def __repr__(self):
        return repr(self.lazycontent)

    def __str__(self):
        return str(self.lazycontent)
