"""Some common utils"""
from time import sleep, time


def countiter(array, start=1, stop=None, w_count=False, v_batch=1, prefix="", suffix="", dft_ind="?"):
    """Iter elems from a while counting

    Args:
        array (iterable)
        start (int)     : count starting point
        stop (int)      : stop iteration when count reaches stop (last included)
        w_count (bool)  : also yield count
        v (int)         : number of iteration b/w displays
        v_batch (int)   : same as v_batch, deprecated
        prefix (string) : count prefix in display
        suffix (string) : count suffix in display
        dft_ind (str)   : string displayed if max count can't be deduced from array

    Return:
        (iterable)
            if w_count: yield (i, elem)
            else: yield elem
    """
    verbose = bool(v_batch)
    try:
        size = len(array) + start - 1
    except TypeError:
        size = dft_ind
    if stop is not None:
        size = f"{stop} (/{size})"

    i = start-1  # ensure existence if no element
    for i, elem in enumerate(array, start):
        if verbose and (i == start or i % v_batch == 0):
            print(f"\r{prefix}{i}/{size}{suffix}", end="")
        yield (i, elem) if w_count else elem
        if (stop is not None) and (i == stop):
            break
    if verbose:
        print(f"\r{prefix}{i}/{size}{suffix}", end="")
        print()


def display(*args, **kwargs):
    """Extension of print with verbose kwarg

    Args:
        v, verbose (bool): whether to print or not
        *args, **kwargs: @see print
    """
    verb1, verb2 = kwargs.pop("v", None), kwargs.pop("verbose", None)
    if isinstance(verb1, bool) and isinstance(verb2, bool):
        raise TypeError(
            "Got multiple values for verbose argument 'v'/'verb2'"
        )
    verb = (
        (verb2 is None or verb2)
        if verb1 is None
        else (verb1 is None or verb1)
    )
    if verb:
        print(*args, **kwargs)


def wait_until(predicate, freq=0.1, timeout=5, raise_err=True):
    """Wait until predicate return True"""
    start = time()
    while not predicate():
        if time() - start > timeout:
            if raise_err:
                raise TimeoutError(
                    "Predicate did not come True before timeout"
                )
            return False
        sleep(freq)
    return True
