from olutils.collection import list as lib


def test_implicit_list():
    assert str(lib.implicit_list([1, 2, 3, 4, 5], 3)) == '[1, ..., 5]'
    assert str(lib.implicit_list([1, 2, 3, 4, 5], 5)) == '[1, 2, 3, 4, 5]'
    assert str(lib.implicit_list([1, 2, 3, 4, 5], 4)) == '[1, 2, ..., 5]'
    assert str(lib.implicit_list([1, 2], 1)) == '[...]'
    assert str(lib.implicit_list([1, 2], 2)) == '[1, 2]'
