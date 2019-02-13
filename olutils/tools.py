"""Some common utils"""


def countiter(a, start=1, w_count=False, v_batch=1, prefix="", suffix=""):
    """Iter elems from a while counting

    Args:
        a (iterable)
        start (int)     : count starting point
        prefix (string) : count prefix in display
        suffix (string) : count suffix in display
        w_count (bool)  : also yield count
        v_batch (int)   : number of iteration b/w displays

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
