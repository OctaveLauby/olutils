from argparse import ArgumentParser
from collections import OrderedDict
import pytest

from olutils import params


def test_check_type():
    assert params.check_type("arg", 1, int) is None
    assert params.check_type("arg", "hello", str) is None
    assert params.check_type("arg", 1., float) is None

    with pytest.raises(TypeError):
        params.check_type("arg", 1, str)

    with pytest.raises(TypeError):
        params.check_type("arg", 1., int)


def test_read_params():
    kwargs = params.read_params({"a": 1}, {"a": 0, "b": 2})
    assert kwargs == {'a': 1, 'b': 2}
    assert kwargs.a == 1
    assert kwargs.b == 2
    kwargs.b = 3
    assert kwargs.b == 3
    assert kwargs == {'a': 1, 'b': 3}

    with pytest.raises(KeyError):
        params.read_params({"a": 1, "c": 3}, {"a": 0, "b": 2})

    kwargs = params.read_params({"a": 1, "c": 3}, {"a": 0, "b": 2}, safe=False)
    assert kwargs == {'a': 1, 'b': 2, 'c': 3}


def test_add_dft_args(capfd):
    parser = ArgumentParser("Test")
    dft_args = OrderedDict([
        ("bool0", False),
        ("bool1", True),
        ("int", 1),
        ("str", "str"),
        ("untyped", None),
    ])
    params.add_dft_args(
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
