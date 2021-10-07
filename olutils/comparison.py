"""Comparison Tools"""
from typing import Hashable, Iterable, Set, TypedDict


class ContentDiff(TypedDict, total=False):
    # Use required/not required keys when available (https://www.python.org/dev/peps/pep-0655/#motivation)
    minus: Set[Hashable]
    plus: Set[Hashable]
    common: Set[Hashable]


def content_diff(
    content1: Iterable[Hashable],
    content2: Iterable[Hashable],
    only_diff: bool = False,
) -> ContentDiff:
    """Return differences b/w contents (list|set|...) in a dictionary

    About:
        Because 0 == False and 1 == True, diff may not work as wanted with
        list mixing booleans and integers.

    Returns:
        (dict) with following items
            'minus', set of elements in content1 and not in content2
            'plus', set of elements in content2 and not in content1
            if not only_diff: 'common', set of common elements
    """
    set1 = set(content1)
    set2 = set(content2)
    common = set1.intersection(set2)
    res = {
        "minus": set1 - common,
        "plus": set2 - common,
    }
    if not only_diff:
        res["common"] = common
    return res
