"""Convenient functions"""

def identity(__object):
    """Identity function"""
    return __object


def prod(iterable, /, start=1):
    """Return the product of a 'start' value (dft: 0) multiplied by iterable

    When the iterable is empty, return the start value.
    This function is intended specifically for use with numeric values and may
    reject non-numeric types.
    """
    res = start
    for obj in iterable:
        res *= obj
    return res
