import os
import shutil

from olutils import files


TMP_DIR = "tmp"
SUB_DIR = os.path.join(TMP_DIR, "1")
LNG_DIR = os.path.join(TMP_DIR, "1", "2", "3")


# --------------------------------------------------------------------------- #
# Setup / Teardown

def setup_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    assert not os.path.isdir(TMP_DIR)


def teardown_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    assert not os.path.isdir(TMP_DIR)


# --------------------------------------------------------------------------- #
# Tests

def test_mkdirs():

    files.mkdirs(TMP_DIR)
    assert os.path.isdir(TMP_DIR)

    files.mkdirs(LNG_DIR)
    assert os.path.isdir(LNG_DIR)

    # No error when trying to build existing directories
    files.mkdirs(TMP_DIR)
    files.mkdirs(LNG_DIR)

    # No error when trying to build empty directory
    files.mkdirs("")


def test_rmdirs():

    # Remove empty directories
    files.mkdirs(LNG_DIR)

    files.rmdirs(LNG_DIR)
    assert os.path.isdir(SUB_DIR)
    assert not os.path.isdir(LNG_DIR)

    files.rmdirs(SUB_DIR)
    assert os.path.isdir(TMP_DIR)
    assert not os.path.isdir(SUB_DIR)

    files.rmdirs(TMP_DIR)
    assert not os.path.isdir(TMP_DIR)

    # Remove directories with sub-dir containing file
    files.mkdirs(LNG_DIR)
    filepath = os.path.join(SUB_DIR, "file.txt")
    with open(filepath, "w+") as file:
        file.write("this is a test")
    assert os.path.isfile(filepath)

    files.rmdirs(TMP_DIR)
    assert not os.path.isdir(TMP_DIR)


def test_sopen():

    # Test write in to build tmp dir
    filepath = os.path.join(TMP_DIR, "file.txt")
    with files.sopen(filepath) as file:
        file.write("this is a test")
    with open(filepath) as file:
        assert file.read() == "this is a test"

    # Test write in to build long dir tree
    filepath = os.path.join(LNG_DIR, "file.txt")
    with files.sopen(filepath) as file:
        file.write("this is a new test")
    with open(filepath) as file:
        assert file.read() == "this is a new test"
