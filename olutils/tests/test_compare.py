from olutils import compare as lib


def test_diff():
    assert lib.content_diff(
        [1, 2, "hi", "bye"], [3, "bye", "bye bye", 2]
    ) == {
        'common': {2, "bye"},
        'minus': {1, "hi"},
        'plus': {3, "bye bye"},
    }
    assert lib.content_diff(
        [1, 2, "hi", "bye"], [3, "bye", "bye bye", 2], only_diff=True
    ) == {
       'minus': {1, "hi"},
       'plus': {3, "bye bye"},
   }
