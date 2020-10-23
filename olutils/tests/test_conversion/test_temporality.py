import numpy as np
import pytest
from datetime import datetime, timedelta

import olutils.conversion as lib
from olutils.conversion.temporality import (
    HOUR,
    DAY,
    YEAR,
)


def test_globals():
    assert HOUR == 3600
    assert DAY == 24 * 3600
    assert YEAR == 365.25 * 24 * 3600


def test_secs2unit():
    hour, year = HOUR, YEAR
    assert lib.secs2unit(hour, "s") == hour
    assert lib.secs2unit(hour, "min") == 60
    assert lib.secs2unit(hour, unit="min") == 60
    assert lib.secs2unit(hour, "hour") == 1
    assert lib.secs2unit(year, "day") == 365.25
    assert lib.secs2unit(year, "month") == 12
    assert lib.secs2unit(year, "year") == 1
    assert lib.secs2unit(4*year, "dt") == datetime(1974, 1, 1)
    assert lib.secs2unit(hour, "td") == timedelta(0, 3600)

    assert lib.secs2unit([60, 750], "min") == [1, 12.5]
    assert lib.secs2unit((60, 750), "min") == (1, 12.5)
    assert lib.secs2unit({60, 750}, "min") == {1, 12.5}

    inp = [75, 3720]
    outputs = {
        'min': [1.25, 62],
        'td': [timedelta(0, 75), timedelta(0, 3720)],
        'dt': [datetime(1970, 1, 1, 0, 1, 15), datetime(1970, 1, 1, 1, 2, 0)],
    }
    for unit, out in outputs.items():
        for ptype in [list, set, tuple]:
            assert lib.secs2unit(ptype(inp), unit) == ptype(out)

        res = lib.secs2unit(iter(inp), unit)
        assert isinstance(res, map)
        assert list(res) == list(out)

        res = lib.secs2unit(np.array(inp), unit)
        assert isinstance(res, map if unit in ['td', 'dt'] else np.ndarray)
        assert list(res) == list(out)

    with pytest.raises(ValueError):
        lib.secs2unit(10,"unknown")

    with pytest.raises(TypeError):
        lib.secs2unit('60', "min")


def test_dt2ts():
    assert lib.dt2ts(datetime(1970, 1, 2)) == DAY


def test_ts2dt():
    assert lib.ts2dt(DAY) == datetime(1970, 1, 2)


def test_str2dt():
    assert lib.str2dt("19700104") == datetime(1970, 1, 4)
    assert lib.str2dt("1970-01-01 08:00:00") == datetime(1970, 1, 1, 8)
    assert lib.str2dt("1970-01-04 00:00:08") == datetime(1970, 1, 4, 0, 0, 8)
