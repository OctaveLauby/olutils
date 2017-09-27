from argparse import ArgumentParser
from collections import OrderedDict
import pytest

from olutils import params


def test_read_params():
    dft_params = {
        1: "un",
        2: "deux",
        3: "trois",
    }

    params_1 = {
        1: "one",
        3: None,
    }
    assert params.read_params(params_1, dft_params) == {
        1: "one",
        2: "deux",
        3: "trois",
    }

    params_2 = {
        2: "dos",
        3: "tres",
    }
    assert params.read_params(params_2, dft_params) == {
        1: "un",
        2: "dos",
        3: "tres",
    }

    params_3 = {
        0: "zero",
        3: "troyes",
        4: "quatre",
    }
    with pytest.raises(KeyError):
        params.read_params(params_3, dft_params)


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
