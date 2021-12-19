"""Convenient functions"""
from typing import Iterable

from olutils.typing import T


def identity(__obj: T, /) -> T:
    """Identity function"""
    return __obj


def prod(iterable: Iterable[T], /, start: int = 1) -> T:
    """Return the product of a 'start' value (dft: 0) multiplied by iterable

    About:
        When the iterable is empty, return the start value.
        This function is intended specifically for use with numeric values
        and may reject non-numeric types.
    """
    res = start
    for obj in iterable:
        res *= obj
    return res
