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
    verb = True if v_batch else False
    try:
        n = len(a) + start - 1
    except TypeError:
        n = "?"

    i = 0
    for i, elem in enumerate(a, start):
        if i == start or i % v_batch == 0:
            display("\r" + prefix + "%s/%s" % (i, n) + suffix, end="", v=verb)
        yield (i, elem) if w_count else elem

    display("\r" + prefix + "%s/%s" % (i, n) + suffix, end="", v=verb)
    display(v=verb)


def display(*args, **kwargs):
    """Extension of print with v kwarg for verbose (False > no print)"""
    verb = kwargs.pop("v", True)
    if verb:
        print(*args, **kwargs)
