import os

import pytest

from olutils.storing import write_txt
import olutils.path as lib


def test_get_next_path_index(tmpdir):
    path_frmt = os.path.join(tmpdir.strpath, "file_{}.txt")
    assert lib.get_next_path_index(path_frmt) == 1
    assert lib.get_next_path_index(path_frmt, start=10) == 10

    write_txt("", path_frmt.format(10))
    assert lib.get_next_path_index(path_frmt) == 1
    assert lib.get_next_path_index(path_frmt, start=10) == 11

    with pytest.raises(ValueError):
        lib.get_next_path("file_{}_{}.txt")

    with pytest.raises(ValueError):
        lib.get_next_path("file.txt")


def test_get_next_path(tmpdir):
    path_frmt = os.path.join(tmpdir.strpath, "file_{}.txt")
    path_frmt_2 = os.path.join(tmpdir.strpath, "file_{:03d}.txt")
    assert lib.get_next_path(path_frmt) == os.path.join(tmpdir.strpath, "file_1.txt")
    assert lib.get_next_path(path_frmt, start=10) == os.path.join(tmpdir.strpath, "file_10.txt")
    assert lib.get_next_path(path_frmt_2) == os.path.join(tmpdir.strpath, "file_001.txt")
    assert lib.get_next_path(path_frmt_2, start=10) == os.path.join(tmpdir.strpath, "file_010.txt")

    write_txt("", path_frmt.format(10))
    assert lib.get_next_path(path_frmt) == os.path.join(tmpdir.strpath, "file_1.txt")
    assert lib.get_next_path(path_frmt, start=10) == os.path.join(tmpdir.strpath, "file_11.txt")
    assert lib.get_next_path(path_frmt_2) == os.path.join(tmpdir.strpath, "file_001.txt")
    assert lib.get_next_path(path_frmt_2, start=10) == os.path.join(tmpdir.strpath, "file_010.txt")

    write_txt("", path_frmt.format(100))
    assert lib.get_next_path(path_frmt) == os.path.join(tmpdir.strpath, "file_1.txt")
    assert lib.get_next_path(path_frmt, start=10) == os.path.join(tmpdir.strpath, "file_11.txt")
    assert lib.get_next_path(path_frmt_2) == os.path.join(tmpdir.strpath, "file_001.txt")
    assert lib.get_next_path(path_frmt_2, start=100) == os.path.join(tmpdir.strpath, "file_101.txt")
