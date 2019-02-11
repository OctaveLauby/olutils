import os

from olutils import files


def test_all():

    dirtree = "_test/1/2/3"
    filepath = os.path.join(dirtree, "file.txt")
    with files.safe_open(filepath) as file:
        file.write("this is a test")
    with open(filepath) as file:
        assert file.read() == "this is a test"
    assert os.path.isdir(dirtree)
    files.rmdirs(dirtree)
    assert not os.path.isdir(dirtree)
