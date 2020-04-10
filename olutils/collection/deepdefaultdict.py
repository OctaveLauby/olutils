"""Extensions of collections.defaultdict w. dict conv. and pretty formatting"""

import collections

from olutils.conversion import basedict, dict2str


class DefaultDict(collections.defaultdict):
    """dict with default factory

    Overload collections.defaultdict
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
        print(self.pstring(*args, **kwargs))


def defaultdict(default_factory, *args, **kwargs):
    """Return defaultdict given the default factory to produce new values"""
    return DefaultDict(default_factory, *args, **kwargs)


def deepdefaultdict(default_factory, depth):
    """Return a multi ladder defaultdict given the depth and the leaf frmt"""
    if depth == 0:
        return default_factory
    if depth == 1:
        return defaultdict(default_factory)
    return defaultdict(lambda: deepdefaultdict(default_factory, depth-1))
