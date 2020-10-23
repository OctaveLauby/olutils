import numpy as np

import olutils as lib


def test_prod():

    assert lib.prod([]) == 1
    assert lib.prod([5, 8, 0.5]) == 20
    assert lib.prod(e for e in [5, 8, 0.5]) == 20

    assert (lib.prod([
        np.array([3, 7]),
        np.array([5, 11]),
    ]) == np.array([15, 77])).all()
