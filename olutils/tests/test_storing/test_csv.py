import os
import pytest
import shutil
from collections import OrderedDict

from olutils import storing


TMP_DIR = "tmp"
MOCK_DIR = os.path.join("olutils", "tests", "mockups")


def assert_content_equal(path, content):
    with open(path) as file:
        assert file.read() == content


def readout(capfd):
    return capfd.readouterr()[0]


# --------------------------------------------------------------------------- #
# Setup / Teardown

def setup_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


def teardown_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


# --------------------------------------------------------------------------- #
# Tests


def test_read_csv(capfd):

    rows = [
        {'col_1': "11", 'col_2': "12", 'col_3': "13"},
        {'col_1': "21", 'col_2': "22", 'col_3': ""},
        {'col_1': "31", 'col_2': "", 'col_3': "33"},  # col_2 should be None
        {'col_1': "forty_one", 'col_2': "forty_two", 'col_3': "forty_three"},
    ]

    # ---- Basic load

    filepath = os.path.join(MOCK_DIR, "base_comma.csv")
    assert list(storing.read_csv(filepath)) == rows

    filepath = os.path.join(MOCK_DIR, "base_semicolon.csv")
    assert list(storing.read_csv(filepath)) == rows

    filepath = os.path.join(MOCK_DIR, "base_tab.csv")
    assert list(storing.read_csv(filepath)) == rows

    filepath = os.path.join(MOCK_DIR, "base_dash.csv")
    with pytest.raises(ValueError):
        storing.read_csv(filepath)

    filepath = os.path.join(MOCK_DIR, "base_dash.csv")
    assert list(storing.read_csv(filepath, delimiter="-")) == rows

    filepath = os.path.join(MOCK_DIR, "base_comma_lg.csv")
    for i, row in enumerate(storing.read_csv(filepath), 1):
        if i in [1, 3, 8]:
            assert row == {
                'index': str(i),
                'name': "in",
                'value': str(100 + 10 * i),
            }
        else:
            assert row == {
                'index': str(i),
                'name': "out",
                'value': str(100 - 10 * i),
            }
        assert readout(capfd) == ""  # Make sure there is no dft display

    # ---- Rows with multiple delimiters

    filepath = os.path.join(MOCK_DIR, "multi_sep.csv")
    assert list(storing.read_csv(filepath)) == [
        OrderedDict([
            ('col, 1', "this;is,col\t1"),
            ('col 2', "col\t2"),
            ('col\t3', "col, 3"),
            ('col, 4', "col, 4"),
        ]),
    ]
    assert list(storing.read_csv(filepath, delimiter=",")) == [
        OrderedDict([
            ('col', "this;is,col\t1;col\t2;col"),
            (' 1;col 2;col\t3;col', " 3;col"),
            (' 4', " 4"),
        ]),
    ]
    assert list(storing.read_csv(filepath, delimiter="\t")) == [
        OrderedDict([
            ('col, 1;col 2;col', "this;is,col\t1;col"),
            ('3;col, 4', "2;col, 3;col, 4"),
        ]),
    ]

    # ---- Playing with display args

    filepath = os.path.join(MOCK_DIR, "base_comma_lg.csv")
    for i, row in storing.read_csv(filepath, w_count=True, v_batch=4):
        assert readout(capfd) == (
            f"\r{i}/?" if (i == 1 or i % 4 == 0) else ""
        )
    assert readout(capfd) == "\r9/?\n"


def test_write_csv():

    filepath = os.path.join(TMP_DIR, "file.txt")

    # ---- Basic writes

    # # Basic write
    storing.write_csv(
        [
            OrderedDict([('col_1', "val_11"), ('col_2', "val_12")]),
            OrderedDict([('col_1', "val_21"), ('col_2', "val_22")]),
        ],
        filepath,
    )
    assert_content_equal(filepath, (
        "col_1,col_2\n"
        "val_11,val_12\n"
        "val_21,val_22\n"
    ))

    # # Pretty header, ;-delimiter and value with delimiter in it
    storing.write_csv(
        [
            OrderedDict([('col_1', "1, one"), ('col_two', "2; two")]),
            OrderedDict([('col_1', "you"), ('col_two', "me")]),
        ],
        filepath,
        delimiter=";",
        pretty=True
    )
    assert_content_equal(filepath, (
        'Col 1;Col Two\n'
        '1, one;"2; two"\n'
        'you;me\n'
    ))

    # # Selective write
    storing.write_csv(
        [
            OrderedDict([('c_1', "v_11"), ('c_2', "v_12"), ('c_3', "v_13")]),
            OrderedDict([('c_1', "v_21"), ('c_2', "v_22"), ('c_3', "v_23")]),
        ],
        filepath,
        fieldnames=["c_3", "c_1"],
        header=["Column 3", "Column 1"],
    )
    assert_content_equal(filepath, (
        "Column 3,Column 1\n"
        "v_13,v_11\n"
        "v_23,v_21\n"
    ))

    # # Empty rows but fieldnames

    storing.write_csv([], filepath, fieldnames=["c_1", "c_2"])
    assert_content_equal(filepath, "c_1,c_2\n")

    # # a row with empty val and None val (handled the same)
    storing.write_csv(
        [
            OrderedDict([('col_1', "val_11"), ('col_2', "val_12")]),
            OrderedDict([('col_1', ""), ('col_2', None)]),
        ],
        filepath,
    )
    assert_content_equal(filepath, (
        "col_1,col_2\n"
        "val_11,val_12\n"
        ",\n"
    ))

    # # a row is missing a key and a row with empty key (no error)
    storing.write_csv(
        [
            OrderedDict([('col_1', "val_11"), ('col_2', "val_12")]),
            OrderedDict([('col_1', "val_21")]),
        ],
        filepath,
    )
    assert_content_equal(filepath, (
        "col_1,col_2\n"
        "val_11,val_12\n"
        "val_21,\n"
    ))

    # ---- ERRORS

    # # Write ref to make sure file is not overwritten
    storing.write_csv([], filepath, fieldnames=['c_1', 'c_2'])

    # # empty iterable
    storing.write_csv([], filepath, fieldnames=['c_1', 'c_2'])
    with pytest.raises(ValueError):
        storing.write_csv([], filepath)
    assert_content_equal(filepath, "c_1,c_2\n")

    # # Fst row not dictionary
    with pytest.raises(TypeError):
        storing.write_csv(["ab", "cd"], filepath)
    assert_content_equal(filepath, "c_1,c_2\n")

    # # rows not iterable on dict
    with pytest.raises(TypeError):
        storing.write_csv({'key': "value"}, filepath)
    assert_content_equal(filepath, "c_1,c_2\n")

    # # fieldnames and header do not have same length
    with pytest.raises(AssertionError):
        storing.write_csv([
            OrderedDict([('col_1', "val_11"), ('col_2', "val_12")]),
            OrderedDict([('col_1', ""), ('col_2', None)]),
        ], filepath, header=["First, Column", "Second Column", "Third Column"])
