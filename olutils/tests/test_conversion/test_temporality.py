import numpy as np
from datetime import datetime, timedelta

from olutils.conversion import temporality


def test_globals():
    assert temporality.HOUR == 3600
    assert temporality.DAY == 24 * 3600
    assert temporality.YEAR == 365.25 * 24 * 3600


def test_convert_seconds():
    hour, year = temporality.HOUR, temporality.YEAR
    assert temporality.convert_seconds(hour, "s") == hour
    assert temporality.convert_seconds(hour, "min") == 60
    assert temporality.convert_seconds(hour, unit="min") == 60
    assert temporality.convert_seconds(hour, "hour") == 1
    assert temporality.convert_seconds(year, "day") == 365.25
    assert temporality.convert_seconds(year, "month") == 12
    assert temporality.convert_seconds(year, "year") == 1
    assert temporality.convert_seconds(4*year, "dt") == datetime(1974, 1, 1)
    assert temporality.convert_seconds(hour, "td") == timedelta(0, 3600)

    assert temporality.convert_seconds([60, 750], "min") == [1, 12.5]
    assert temporality.convert_seconds((60, 750), "min") == (1, 12.5)
    assert temporality.convert_seconds({60, 750}, "min") == {1, 12.5}

    inp = [75, 3720]
    outputs = {
        'min': [1.25, 62],
        'td': [timedelta(0, 75), timedelta(0, 3720)],
        'dt': [datetime(1970, 1, 1, 0, 1, 15), datetime(1970, 1, 1, 1, 2, 0)],
    }
    for unit, out in outputs.items():
        for ptype in [list, set, tuple]:
            assert temporality.convert_seconds(ptype(inp), unit) == ptype(out)

        res = temporality.convert_seconds(iter(inp), unit)
        assert isinstance(res, map)
        assert list(res) == list(out)

        res = temporality.convert_seconds(np.array(inp), unit)
        assert isinstance(res, map if unit in ['td', 'dt'] else np.ndarray)
        assert list(res) == list(out)


def test_dt2ts():
    assert temporality.dt2ts(datetime(1970, 1, 2)) == temporality.DAY


def test_ts2dt():
    assert temporality.ts2dt(temporality.DAY) == datetime(1970, 1, 2)


def test_str2dt():
    assert temporality.str2dt("19700104") == datetime(1970, 1, 4)
    assert temporality.str2dt("1970-01-01 08:00:00") == datetime(1970, 1, 1, 8)
    assert temporality.str2dt("1970-01-04 00:00:08") == datetime(1970, 1, 4, 0, 0, 8)
