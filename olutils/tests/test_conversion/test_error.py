import olutils as lib


def test_err2str():
    assert lib.err2str(ValueError("Some Message")) == "ValueError - Some Message"
    assert lib.err2str(ValueError("Some Message"), msg_only=True) == "Some Message"
