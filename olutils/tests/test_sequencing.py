import numpy as np
import pytest

from olutils import sequencing as lib


def readout(capfd):
    return capfd.readouterr()[0]


def test_countiter(capfd):

    for i, elem in enumerate(lib.countiter([1, 2, 3]), 1):
        assert elem == i
        assert readout(capfd) == f"\r{i}/3"
    assert readout(capfd) == "\r3/3\n"

    for i, elem in lib.countiter([1, 2, 3], w_count=True):
        assert elem == i
        assert readout(capfd) == f"\r{i}/3"
    assert readout(capfd) == "\r3/3\n"

    for i, elem in lib.countiter([1, 2, 3], w_count=True, start=2):
        assert elem == i-1
        assert readout(capfd) == f"\r{i}/4"
    assert readout(capfd) == "\r4/4\n"

    for i, elem in lib.countiter(iter([1, 2, 3]), w_count=True, start=0):
        assert elem == i+1
        assert readout(capfd) == f"\r{i}/?"
    assert readout(capfd) == "\r2/?\n"

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    iterator = lib.countiter(
        alphabet, w_count=True, prefix="> ", suffix=" <", vbatch=5,
    )
    for i, elem in iterator:
        assert elem == alphabet[i-1]
        if i == 1 or i % 5 == 0:
            assert readout(capfd) == f"\r> {i}/26 <"
        else:
            assert readout(capfd) == ""
    assert readout(capfd) == "\r> 26/26 <\n"

    for i, elem in lib.countiter([1, 2, 3], w_count=True, vbatch=0):
        assert elem == i
        assert readout(capfd) == ""
    assert readout(capfd) == ""

    for i, elem in lib.countiter([1, 2, 3], w_count=True, vbatch=None):
        assert elem == i
        assert readout(capfd) == ""
    assert readout(capfd) == ""

    aggregator = []
    for i, elem in lib.countiter([1, 2, 3], stop=2, w_count=True):
        aggregator.append(elem)
        assert readout(capfd) == f"\r{i}/2 (/3)"
    assert aggregator == [1, 2]
    assert readout(capfd) == f"\r{2}/2 (/3)\n"




def test_display(capfd):

    msg = "this is a test"

    lib.display(msg)
    assert readout(capfd) == msg + "\n"

    lib.display(msg, verbose=True)
    assert readout(capfd) == msg + "\n"

    lib.display(msg, verbose=False)
    assert readout(capfd) == ""

    lib.display(msg, v=True)
    assert readout(capfd) == msg + "\n"

    lib.display(msg, v=False)
    assert readout(capfd) == ""

    with pytest.raises(TypeError):
        lib.display(msg, verbose=True, v=True)

    with pytest.raises(TypeError):
        lib.display(msg, verbose=True, v=False)

    with pytest.raises(TypeError):
        lib.display(msg, verbose=False, v=True)

    with pytest.raises(TypeError):
        lib.display(msg, verbose=False, v=False)

    lib.display(msg, verbose=False, v=None)
    assert readout(capfd) == ""

    lib.display(msg, verbose=None, v=False)
    assert readout(capfd) == ""
