import olutils.collection as lib


def test_FlatStr():
    assert repr(lib.FlatStr("Hello")) == "Hello"
