"""Convenient functions"""
from typing import Any, Iterable


def identity(__object: Any, /):
    """Identity function"""
    return __object


def prod(iterable: Iterable, /, start: int = 1):
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
