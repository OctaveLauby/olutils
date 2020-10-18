"""List conversion"""
from .spestr import SpeStr


def lazy_content(l, max_values, mid_value=SpeStr('...')):
    """Return lazy content of list, with at most max_values

    Extra values are replaced with mid_value


    Examples:
        >>> lazy_content([1, 2, 3, 4, 5], 3)
        ... [1, ..., 5]
    """
    if len(l) <= max_values:
        return l
    else:
        return (
                l[:max_values // 2]
                + [mid_value]
                + l[len(l) - abs(max_values - 1) // 2:]
        )


class LazyList:
    """List with lazy representation"""

    def __init__(self, l, max_values, mid_value=SpeStr('...')):
        self._content = list(l)
        self.maxvals = max_values
        self.midval = mid_value

    @property
    def content(self):
        return self._content

    @property
    def lazycontent(self):
        """Lazy content list"""
        return lazy_content(
            self.content,
            max_values=self.maxvals,
            mid_value=self.midval,
        )

    def append(self, __object):
        return self.content.append(__object)

    def insert(self, __index, __object):
        return self.content.insert(__index, __object)

    def __len__(self):
        return len(self.content)

    def __repr__(self):
        return repr(self.lazycontent)

    def __str__(self):
        return str(self.lazycontent)
