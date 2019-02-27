"""Some common utils"""


def countiter(a, start=1, w_count=False, v_batch=1, prefix="", suffix=""):
    """Iter elems from a while counting

    Args:
        a (iterable)
        start (int)     : count starting point
        w_count (bool)  : also yield count
        v_batch (int)   : number of iteration b/w displays
        prefix (string) : count prefix in display
        suffix (string) : count suffix in display

    Return:
        (iterable)
            if w_count: yield (i, elem)
            else: yield elem
    """
    verbose = True if v_batch else False
    try:
        n = len(a) + start - 1
    except TypeError:
        n = "?"

    i = 0
    for i, elem in enumerate(a, start):
        if verbose and (i == start or i % v_batch == 0):
            print("\r" + prefix + "%s/%s" % (i, n) + suffix, end="")
        yield (i, elem) if w_count else elem

    if verbose:
        print("\r" + prefix + "%s/%s" % (i, n) + suffix, end="")
        print()


def diff(list1, list2):
    """Return diff b/w lists in a dictionary

    About:
        Because 0 == False and 1 == True, diff may not work as wanted with
        list mixing booleans and integers.

    Return:
        (dict) with following items
            'common', set of common elements
            'minus', set of elements in list1 and not in list2
            'plus', set of elements in list2 and not in list1
    """
    s1 = set(list1)
    s2 = set(list2)
    common = s1.intersection(s2)
    return {
        'common': common,
        'minus': s1 - common,
        'plus': s2 - common,
    }


def display(*args, **kwargs):
    """Extension of print with verbose kwarg

    Args:
        v, verbose (bool): whether to print or not
        *args, **kwargs: @see print
    """
    v, verbose = kwargs.pop("v", None), kwargs.pop("verbose", None)
    if isinstance(v, bool) and isinstance(verbose, bool):
        raise TypeError(
            "Got multiple values for verbose argument 'v'/'verbose'"
        )
    verb = (
        (verbose is None or verbose)
        if v is None
        else (v is None or v)
    )
    if verb:
        print(*args, **kwargs)
