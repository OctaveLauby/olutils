"""Search functions."""


def closest(values, elements, scope=None, strict=True):
    """Return closest (index, elem) of sorted values

    If 2 elements have same distance to a given value, second elem will be
        return has closest.

    Example:
        > closest([1, 4], [0, 2, 3])
        [(1, 2), (2, 3)]
    """
    res = []

    def add(val, index, elem):
        """Add elem to res"""
        diff = abs(elem - val)
        if scope is None:
            res.append((index, elem))
        elif diff < scope if strict else diff <= scope:
            res.append((index, elem))
        else:
            res.append((None, None))

    elem_iter = iter(elements)
    val_iter = iter(values)

    try:
        elem = next(elem_iter)
        val = next(val_iter)
        index = 0
    except StopIteration:
        raise ValueError("Can look for closest is values or elements is empty")

    last_diff, last_elem = abs(elem - val), elem

    while True:
        diff = abs(elem - val)
        if diff <= last_diff:
            last_diff, last_elem = diff, elem
            try:
                elem = next(elem_iter)
            except StopIteration:
                elem = None
                break
            index += 1
        else:
            add(val, index - 1, last_elem)
            try:
                val = next(val_iter)
            except StopIteration:
                val = None
                break
            last_diff = abs(last_elem - val)

    if elem is None:
        add(val, index, last_elem)
        for val in val_iter:
            add(val, index, last_elem)

    return res


def previous(values, elements, scope=None, strict=True):
    """Return closest previous (index, elem) of values withing scope.

    Assumption:
        values and elements are sorted
    """

    # Init iterator on elements
    elem_indexes = enumerate(elements)
    index, elem = next(elem_indexes)
    try:
        nindex, nelem = next(elem_indexes)
    except StopIteration:
        nindex, nelem = None, None

    # Build results
    res = []
    for val in values:

        # No previous val
        if val < elem:
            res.append((None, None))
            continue

        # Get closest previous elem
        try:
            while nelem is not None and val >= nelem:
                index, elem = nindex, nelem
                nindex, nelem = next(elem_indexes)
        except StopIteration:
            pass

        # Check thld
        if scope is None:
            res.append((index, elem))
            continue

        thld = elem + scope
        if val < thld if strict else val <= thld:
            res.append((index, elem))
        else:
            res.append((None, None))

    return res
