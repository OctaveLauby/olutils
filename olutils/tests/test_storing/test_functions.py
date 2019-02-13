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

    path_frmt = os.path.join(TMP_DIR, "obj.{}")

    for mthd in ["json", "pickle"]:
        path = path_frmt.format(mthd)
        storing.save(obj, path)
        assert storing.load(path) == obj

    path = path_frmt.format("unk")
    with pytest.raises(ValueError):
        storing.save(obj, path)
    storing.save(obj, path, mthd="json")

    with pytest.raises(ValueError):
        storing.load(path)
    assert storing.load(path, mthd="json") == obj

    # TODO : more testing
