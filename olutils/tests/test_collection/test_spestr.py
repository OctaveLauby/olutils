import olutils.collection as lib


def test_SpeStr():
    assert repr(lib.SpeStr("Hello")) == "Hello"