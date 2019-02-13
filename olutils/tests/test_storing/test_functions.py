import os
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

    obj = {
        "1": 1, "2": 2,
    }

    path_json = os.path.join(TMP_DIR, "obj.json")
    path_pickle = os.path.join(TMP_DIR, "obj.pickle")
    path_unk = os.path.join(TMP_DIR, "obj.unk")

    storing.save(obj, path_json)
    storing.save(obj, path_pickle)
    with pytest.raises(ValueError):
        storing.save(obj, path_unk)
    storing.save(obj, path_unk, mthd="json")

    assert storing.load(path_json) == obj
    assert storing.load(path_pickle) == obj
    assert storing.load(path_unk, mthd="json") == obj
