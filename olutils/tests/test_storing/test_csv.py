import os
import pytest
import shutil
from collections import OrderedDict

from olutils import storing


TMP_DIR = "tmp"


def assert_content_equal(path, content):
    with open(path) as file:
        assert file.read() == content


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


def test_write_csv():

    filepath = os.path.join(TMP_DIR, "file.txt")

    # ---- Basic writes

    # # Basic write
    storing.write_csv(
        [
            OrderedDict([("col_1", "val_11"), ("col_2", "val_12")]),
            OrderedDict([("col_1", "val_21"), ("col_2", "val_22")]),
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
            OrderedDict([("col_1", "1, one"), ("col_two", "2; two")]),
            OrderedDict([("col_1", "you"), ("col_two", "me")]),
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
            OrderedDict([("c_1", "v_11"), ("c_2", "v_12"), ("c_3", "v_13")]),
            OrderedDict([("c_1", "v_21"), ("c_2", "v_22"), ("c_3", "v_23")]),
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

    # # a row is missing a key
    storing.write_csv(
        [
            OrderedDict([("col_1", "val_11"), ("col_2", "val_12")]),
            OrderedDict([("col_1", "val_21")]),
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
    storing.write_csv([], filepath, fieldnames=["c_1", "c_2"])

    # # empty iterable
    storing.write_csv([], filepath, fieldnames=["c_1", "c_2"])
    with pytest.raises(ValueError):
        storing.write_csv([], filepath)
    assert_content_equal(filepath, "c_1,c_2\n")

    # # Fst row not dictionary
    with pytest.raises(TypeError):
        storing.write_csv(["ab", "cd"])
    assert_content_equal(filepath, "c_1,c_2\n")

    # # rows not iterable on dict
    with pytest.raises(TypeError):
        storing.write_csv({'key': "value"})
    assert_content_equal(filepath, "c_1,c_2\n")
