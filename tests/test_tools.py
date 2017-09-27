import os
import pytest
import shutil

from olutils import tools


TMP_DIR = "tmp"


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

def test_copy():

    dictionary = {
        "int": 1,
        "dict": {
            "int-list": [1, 2, 3],
            "dict-list": [
                {"int": 1},
                {"int-list": [0, 1, 2]},
            ],
        },
    }
    cdict = tools.copy(dictionary)
    cdict["int"] = 13
    cdict["dict"]["int-list"].append(4)
    cdict["dict"]["dict-list"][1]["int-list"].append(3)

    assert dictionary == {
        "int": 1,
        "dict": {
            "int-list": [1, 2, 3],
            "dict-list": [
                {"int": 1},
                {"int-list": [0, 1, 2]},
            ],
        },
    }
    assert cdict == {
        "int": 13,
        "dict": {
            "int-list": [1, 2, 3, 4],
            "dict-list": [
                {"int": 1},
                {"int-list": [0, 1, 2, 3]},
            ],
        },
    }


def test_save_load():

    obj = {
        "1": 1, "2": 2,
    }

    path_json = os.path.join(TMP_DIR, "obj.json")
    path_pickle = os.path.join(TMP_DIR, "obj.pickle")
    path_unk = os.path.join(TMP_DIR, "obj.unk")

    tools.save(obj, path_json)
    tools.save(obj, path_pickle)
    with pytest.raises(ValueError):
        tools.save(obj, path_unk)
    tools.save(obj, path_unk, method="json")

    assert tools.load(path_json) == obj
    assert tools.load(path_pickle) == obj
    assert tools.load(path_unk, method="json") == obj
