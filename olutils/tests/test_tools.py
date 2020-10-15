import numpy as np
import pytest

from olutils import tools


def readout(capfd):
    return capfd.readouterr()[0]


def test_countiter(capfd):

    for i, elem in enumerate(tools.countiter([1, 2, 3]), 1):
        assert elem == i
        assert readout(capfd) == f"\r{i}/3"
    assert readout(capfd) == "\r3/3\n"

    for i, elem in tools.countiter([1, 2, 3], w_count=True):
        assert elem == i
        assert readout(capfd) == f"\r{i}/3"
    assert readout(capfd) == "\r3/3\n"

    for i, elem in tools.countiter([1, 2, 3], w_count=True, start=2):
        assert elem == i-1
        assert readout(capfd) == f"\r{i}/4"
    assert readout(capfd) == "\r4/4\n"

    for i, elem in tools.countiter(iter([1, 2, 3]), w_count=True, start=0):
        assert elem == i+1
        assert readout(capfd) == f"\r{i}/?"
    assert readout(capfd) == "\r2/?\n"

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    iterator = tools.countiter(
        alphabet, w_count=True, prefix="> ", suffix=" <", v_batch=5,
    )
    for i, elem in iterator:
        assert elem == alphabet[i-1]
        if i == 1 or i % 5 == 0:
            assert readout(capfd) == f"\r> {i}/26 <"
        else:
            assert readout(capfd) == ""
    assert readout(capfd) == "\r> 26/26 <\n"

    for i, elem in tools.countiter([1, 2, 3], w_count=True, v_batch=0):
        assert elem == i
        assert readout(capfd) == ""
    assert readout(capfd) == ""

    for i, elem in tools.countiter([1, 2, 3], w_count=True, v_batch=None):
        assert elem == i
        assert readout(capfd) == ""
    assert readout(capfd) == ""

    aggregator = []
    for i, elem in tools.countiter([1, 2, 3], stop=2, w_count=True):
        aggregator.append(elem)
        assert readout(capfd) == f"\r{i}/2 (/3)"
    assert aggregator == [1, 2]
    assert readout(capfd) == f"\r{2}/2 (/3)\n"


def test_diff():
    assert tools.diff(
        [1, 2, "hi", "bye"], [3, "bye", "bye bye", 2]
    ) == {
        'common': {2, "bye"},
        'minus': {1, "hi"},
        'plus': {3, "bye bye"},
    }


def test_display(capfd):

    msg = "this is a test"

    tools.display(msg)
    assert readout(capfd) == msg + "\n"

    tools.display(msg, verbose=True)
    assert readout(capfd) == msg + "\n"

    tools.display(msg, verbose=False)
    assert readout(capfd) == ""

    tools.display(msg, v=True)
    assert readout(capfd) == msg + "\n"

    tools.display(msg, v=False)
    assert readout(capfd) == ""

    with pytest.raises(TypeError):
        tools.display(msg, verbose=True, v=True)

    with pytest.raises(TypeError):
        tools.display(msg, verbose=True, v=False)

    with pytest.raises(TypeError):
        tools.display(msg, verbose=False, v=True)

    with pytest.raises(TypeError):
        tools.display(msg, verbose=False, v=False)

    tools.display(msg, verbose=False, v=None)
    assert readout(capfd) == ""

    tools.display(msg, verbose=None, v=False)
    assert readout(capfd) == ""


def test_prod():

    assert tools.prod([]) == 1
    assert tools.prod([5, 8, 0.5]) == 20
    assert tools.prod(e for e in [5, 8, 0.5]) == 20

    assert (tools.prod([
        np.array([3, 7]),
        np.array([5, 11]),
    ]) == np.array([15, 77])).all()
