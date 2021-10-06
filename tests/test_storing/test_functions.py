import os
import pickle
import pytest
import shutil

import olutils as lib


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


def test_save_load():

    obj = [
        {"1": 1, "2": 2},
        {"1": 10, "2": 20},
        {"1": -1, "2": -2},
    ]

    path_frmt = os.path.join(TMP_DIR, "__object.{}")

    for mthd in ["csv", "json", "pickle"]:
        path = path_frmt.format(mthd)
        lib.save(obj, path)
        if mthd == "csv":
            assert list(lib.load(path)) == [
                {key: str(val) for key, val in row.items()}
                for row in obj
            ]
        else:
            assert lib.load(path) == obj

    path = path_frmt.format("unk")
    with pytest.raises(ValueError):
        lib.save(obj, path)

    lib.save(obj, path, mthd="json")
    with pytest.raises(ValueError):
        lib.load(path)
    with pytest.raises(pickle.UnpicklingError):
        lib.load(path, mthd="pickle")
    assert lib.load(path, mthd="json") == obj

    # Test txt load and save
    content = "some text"
    path = path_frmt.format("txt")
    lib.save(content, path)
    assert lib.load(path, rtype=str) == content
    lib.save([content], path, has_eol=False)
    assert lib.load(path) == [content+"\n"]
