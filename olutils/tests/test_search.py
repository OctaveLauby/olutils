from datetime import datetime, timedelta
from dateutil.parser import parse

from olutils import search


def test_closest():
    assert search.closest([0.4], [0, 1, 3]) == [
        (0, 0)
    ]
    assert search.closest([1, 4, 6, 7], [0, 1, 3]) == [
        (1, 1), (2, 3), (2, 3), (2, 3)
    ]
    assert search.closest([-2, -1, 0, 1, 2], [0, 1, 3]) == [
        (0, 0), (0, 0), (0, 0), (1, 1), (2, 3)
    ]
    assert search.closest(
        [-3, 0, 3, 6, 9], [2, 4], scope=2, strict=False
    ) == [
        (None, None), (0, 2), (1, 4), (1, 4), (None, None)
    ]
    assert search.closest(
        [-3, 0, 3, 6, 9], [2, 4, 6], scope=2, strict=True
    ) == [
        (None, None), (None, None), (1, 4), (2, 6), (None, None)
    ]

    elements = [
        parse('2017-04-10T00:00:00+02:00'),
        parse('2017-04-10T00:10:00+02:00'),
        parse('2017-04-10T00:20:00+02:00'),
        parse('2017-04-10T00:30:00+02:00'),
        parse('2017-04-10T00:40:00+02:00'),
        parse('2017-04-10T00:50:00+02:00'),
        parse('2017-04-10T01:00:00+02:00'),
    ]

    values = [
        parse('2017-04-10T00:00:00+02:00'),
        parse('2017-04-10T00:40:00+02:00'),
        parse('2017-04-10T00:50:00+02:00'),
    ]

    assert search.closest(values, elements) == [
        (0, parse('2017-04-10T00:00:00+02:00')),
        (4, parse('2017-04-10T00:40:00+02:00')),
        (5, parse('2017-04-10T00:50:00+02:00')),
    ]

    elements = [
        datetime(2017, 4, 10) + timedelta(seconds=10*60*i) for i in range(20)
    ]
    assert search.closest(elements, elements) == list(enumerate(elements))


def test_previous():

    assert search.previous([1, 5], [0, 2, 4], scope=1, strict=False) == [
        (0, 0), (2, 4)
    ]
    assert search.previous([1, 5], [0, 2, 4], scope=1) == [
        (None, None), (None, None)
    ]
    assert search.previous([1, 5], [2, 4, 6], scope=2) == [
        (None, None), (1, 4)
    ]
    assert search.previous([1, 5, 9], [0, 2], scope=2) == [
        (0, 0), (None, None), (None, None)
    ]
    assert search.previous(
        [1, 2, 3, 4, 5], [0, 2, 4, 6], scope=2, strict=False
    ) == [
        (0, 0), (1, 2), (1, 2), (2, 4), (2, 4)
    ]
    assert search.previous([1, 2, 3, 4], [2.5]) == [
        (None, None), (None, None), (0, 2.5), (0, 2.5)
    ]
