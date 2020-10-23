import olutils as lib


def test_build_lazy_content():
    assert str(lib.lazy_content([1, 2, 3, 4, 5], 3)) == '[1, Ellipsis, 5]'
    assert str(lib.lazy_content([1, 2, 3, 4, 5], 5)) == '[1, 2, 3, 4, 5]'
    assert str(lib.lazy_content([1, 2, 3, 4, 5], 4)) == '[1, 2, Ellipsis, 5]'
    assert str(lib.lazy_content([1, 2], 1)) == '[Ellipsis]'
    assert str(lib.lazy_content([1, 2], 2)) == '[1, 2]'


def test_LazyList():


    ll = lib.LazyList([1, 2, 3, 4, 5], 3)
    assert len(ll) == 5
    assert str(ll) == '[1, Ellipsis, 5]'
    assert repr(ll) == '[1, Ellipsis, 5]'
    ll.append(6)
    ll.insert(0, 0)
    assert str(ll) == '[0, Ellipsis, 6]'
