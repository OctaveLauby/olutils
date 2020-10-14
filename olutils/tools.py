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
    set1 = set(list1)
    set2 = set(list2)
    common = set1.intersection(set2)
    return {
        'common': common,
        'minus': set1 - common,
        'plus': set2 - common,
    }


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



def identity(object):
    """Identity function"""
    return object


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
