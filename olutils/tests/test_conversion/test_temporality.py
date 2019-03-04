from datetime import datetime

from olutils.conversion import temporality


DAY = 86400


def test_dt2float():
    assert temporality.dt2float(datetime(1970, 1, 2)) == DAY


def test_float2dt():
    assert temporality.float2dt(DAY) == datetime(1970, 1, 2)


def test_str2dt():
    assert temporality.str2dt("19700104") == datetime(1970, 1, 4)
    assert temporality.str2dt("1970-01-01 08:00:00") == datetime(1970, 1, 1, 8)
    assert temporality.str2dt("1970-01-04 00:00:08") == datetime(1970, 1, 4, 0, 0, 8)
