from datetime import datetime

from olutils.conversion import dt


DAY = 86400


def test_dt2float():
    assert dt.dt2float(datetime(1970, 1, 2)) == DAY


def test_float2dt():
    assert dt.float2dt(DAY) == datetime(1970, 1, 2)


def test_str2dt():
    assert dt.str2dt("19700104") == datetime(1970, 1, 4)
    assert dt.str2dt("1970-01-01 08:00:00") == datetime(1970, 1, 1, 8)
    assert dt.str2dt("1970-01-04 00:00:08") == datetime(1970, 1, 4, 0, 0, 8)
