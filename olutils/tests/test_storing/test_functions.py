import os
import pickle
import pytest
import shutil

from olutils import storing


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
        storing.save(obj, path)
        if mthd == "csv":
            assert list(storing.load(path)) == [
                {key: str(val) for key, val in row.items()}
                for row in obj
            ]
        else:
            assert storing.load(path) == obj

    path = path_frmt.format("unk")
    with pytest.raises(ValueError):
        storing.save(obj, path)

    storing.save(obj, path, mthd="json")
    with pytest.raises(ValueError):
        storing.load(path)
    with pytest.raises(pickle.UnpicklingError):
        storing.load(path, mthd="pickle")
    assert storing.load(path, mthd="json") == obj

    # Test txt load and save
    content = "some text"
    path = path_frmt.format("txt")
    storing.save(content, path)
    assert storing.load(path, rtype=str) == content
    storing.save([content], path, has_eol=False)
    assert storing.load(path) == [content+"\n"]
