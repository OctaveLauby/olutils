import os
import shutil
from collections import OrderedDict

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

def test_write_csv():

    filepath = os.path.join(TMP_DIR, "file.txt")

    storing.write_csv(
        [
            OrderedDict([("col_1", "1, one"), ("col_two", "2; two")]),
            OrderedDict([("col_1", "you"), ("col_two", "me")]),
        ],
        filepath,
        delimiter=";",
        pretty=True
    )
    with open(filepath) as file:
        assert file.read() == (
            'Col 1;Col Two\n'
            '1, one;"2; two"\n'
            'you;me\n'
        )
