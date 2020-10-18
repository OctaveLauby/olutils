"""List conversion"""
from olutils.collection import SpeStr


def implicit_list(l, max_values, mid_value=SpeStr('...')):
    """Return implicit list of l, with at most max_values

    Extra values are replaced with mid_value


    Examples:
        >>> implicit_list([1, 2, 3, 4, 5], 3)
        ... [1, ..., 5]
    """
    if len(l) <= max_values:
        return l
    else:
        return l[:max_values//2] + [mid_value] + l[len(l)-abs(max_values-1)//2:]
