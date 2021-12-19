"""Extension of collections.defaultdict"""
from collections import defaultdict as ddict
from typing import Dict, Optional

from olutils.typing import Factory
from olutils.conversion.dictionary import basedict, dict2str


class DefaultDict(ddict):
    """dict with default factory

    Overload collections.defaultdict conversion to base dictionary and pretty
    formatting.
    """

    def to_dict(self) -> Dict:
        """Return base dictionary from instance"""
        return basedict(self)

    def pstring(self, *args, **kwargs) -> str:
        """Return pretty string of instance

        Args:
            *args, **kwargs: @see `~olutils.dict2str`
        """
        return dict2str(self, *args, **kwargs)

    def pprint(self, *args, **kwargs):
        """Pretty print self

        Args:
            *args, **kwargs: @see `~olutils.dict2str`
        """
        print(self.pstring(*args, **kwargs))


def defaultdict(default_factory: Factory, *args, **kwargs) -> DefaultDict:
    """Return defaultdict given the default factory to produce new values"""
    return DefaultDict(default_factory, *args, **kwargs)


def deepdefaultdict(default_factory: Factory, depth: int) -> Optional[DefaultDict]:
    """Return a multi ladder defaultdict given the leaf factory and depth"""
    if depth < 0:
        return None
    if depth == 0:
        return default_factory()
    if depth == 1:
        return defaultdict(default_factory)
    return defaultdict(lambda: deepdefaultdict(default_factory, depth - 1))
