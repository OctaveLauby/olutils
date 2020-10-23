from argparse import ArgumentParser
from collections import OrderedDict
import pytest

import olutils as lib
import olutils.params as lib2


def test_check_type():
    assert lib2.check_type("arg", 1, int) is None
    assert lib2.check_type("arg", "hello", str) is None
    assert lib2.check_type("arg", 1., float) is None

    with pytest.raises(TypeError):
        lib2.check_type("arg", 1, str)

    with pytest.raises(TypeError):
        lib2.check_type("arg", 1., int)


def test_read_params():

    # ---- Single default kwargs
    kwargs = lib.read_params({'a': 0}, {'a': 1, 'b': 2})
    assert kwargs == {'a': 0, 'b': 2}
    assert kwargs.a == 0
    assert kwargs.b == 2
    kwargs.b = 3
    assert kwargs.b == 3
    assert kwargs == {'a': 0, 'b': 3}

    with pytest.raises(KeyError):
        lib.read_params({'a': 0, 'c': 8}, {'a': 1, 'b': 2})

    kwargs = lib.read_params({'a': 0, 'c': 8}, {'a': 1, 'b': 2}, safe=False)
    assert kwargs == {'a': 0, 'b': 2}

    kwargs = lib.read_params(
        {'a': lib.DFT, 'b': None}, {'a': 1, 'b': 2}
    )
    assert kwargs == {'a': 1, 'b': None}


    # ---- Multiple default kwargs
    kwargs = lib.read_params(
        {'a': 0, 'c': 8}, [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}],
    )
    assert kwargs == [{'a': 0, 'b': 2}, {"c": 8, "d": 4}]

    with pytest.raises(KeyError):
        lib.read_params(
            {'a': 0, 'c': 8, 'e': 10}, [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}],
        )

    kwargs = lib.read_params(
        {'a': 0, 'c': 8, 'e': 10},
        [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}],
        safe=False
    )
    assert kwargs == [{'a': 0, 'b': 2}, {'c': 8, 'd': 4}]

    kwargs = lib.read_params(
        {'a': 0, 'c': 8, 'e': 10},
        [{'a': 1, 'b': 2, 'e': 5, 'f': 6}, {'c': 3, 'd': 4, 'e': 5, 'f': 7}],
        safe=False
    )
    assert kwargs == [
        {'a': 0, 'b': 2, 'e': 10, 'f': 6},
        {'c': 8, 'd': 4, 'e': 10, 'f': 7},
    ]


def test_add_dft_args(capfd):
    parser = ArgumentParser("Test")
    dft_args = OrderedDict([
        ("bool0", False),
        ("bool1", True),
        ("int", 1),
        ("str", "str"),
        ("untyped", None),
    ])
    lib2.add_dft_args(
        parser,
        dft_args,
        flag_prefix="f_",
        help_prefix="h - "
    )

    parser.print_help()
    out, err = capfd.readouterr()
    assert out == (
        "usage: Test [-h] [--f_bool0] [--f_bool1] [--f_int F_INT] [--f_str F_STR]"
        "\n            [--f_untyped F_UNTYPED]"
        "\n"
        "\noptional arguments:"
        "\n  -h, --help            show this help message and exit"
        "\n  --f_bool0             h - bool0"
        "\n  --f_bool1             h - bool1"
        "\n  --f_int F_INT         h - int, default is 1"
        "\n  --f_str F_STR         h - str, default is str"
        "\n  --f_untyped F_UNTYPED"
        "\n                        h - untyped, default is None"
        "\n"
    )
