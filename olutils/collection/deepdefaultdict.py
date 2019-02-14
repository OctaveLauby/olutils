import collections

from olutils.conversion import basedict, dict2str


class defaultdict(collections.defaultdict):
    """dict with default factory

    Overloading over collections.defaultdict
    """
    def to_dict(self):
        """Return base dictionary from self"""
        return basedict(self)

    def pstring(self, *args, **kwargs):
        """Return pretty string of self

        Args:
            *args, **kwargs: @see olutils.conversion.dict2str

        Return:
            (str)
        """
        return dict2str(self, *args, **kwargs)

    def pprint(self, *args, **kwargs):
        """Pretty print self

        Args:
            *args, **kwargs: @see olutils.conversion.dict2str
        """
        print(self.dict2str(*args, **kwargs))


def deepdefaultdict(item_frmt, depth):
    """Return a multi ladder defaultdict given the depth and the leaf frmt"""
    if depth == 0:
        return item_frmt
    elif depth == 1:
        return defaultdict(item_frmt)
    else:
        return defaultdict(lambda: deepdefaultdict(item_frmt, depth-1))
