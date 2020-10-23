"""Functions for sequencing"""
from time import sleep, time


def countiter(iterable, /, start=1, stop=None, *,
              w_count=False, vbatch=1, prefix="", suffix="", dindicator="?"):
    """Iterate elements from a while counting

    Args:
        iterable (iterable)
        start (int)     : count starting point
        stop (int)      : stop iteration when count reaches stop (last included)
        w_count (bool)  : also yield count
        vbatch (int)    : number of iteration b/w progress displays
            0 for no display
        prefix (string) : count prefix in display
        suffix (string) : count suffix in display
        dindicator (str): default indicator for max count
            used when object has no readable length

    Return:
        (iterable)
            if w_count: yield (i, elem)
            else: yield elem
    """
    verbose = bool(vbatch)
    try:
        size = len(iterable) + start - 1
    except TypeError:
        size = dindicator
    if stop is not None:
        size = f"{stop} (/{size})"

    i = start-1  # ensure existence if no element
    for i, elem in enumerate(iterable, start):
        if verbose and (i == start or i % vbatch == 0):
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


def wait_until(predicate, *, freq=0.1, timeout=5, raise_err=True):
    """Wait until predicate return True

    Args:
        predicate (callable)
        freq (int|float): number of seconds b/w checks of predicate
        timeout (int|float): max number of seconds to wait
        raise_err (bool): raise error if timeout reached

    Raise:
        (TimeoutError): raise_err is True & timeout reached

    Return:
        (bool): whether predicate returned True
    """
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
