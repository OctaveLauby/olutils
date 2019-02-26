"""Convenient converters"""
from datetime import datetime, timedelta
from dateutil.parser import parse

DATE_REF = datetime(1970, 1, 1)


def dt2float(dt):
    """Return seconds since the Unix Epoch"""
    return (dt-DATE_REF).total_seconds()


def float2dt(nb):
    """Return datetime from seconds since the Unix Epoch"""
    return DATE_REF + timedelta(seconds=nb)


def dtref2float(dateref, timeref):
    """Build datetime from date and time reference

    Args:
        dateref (str): date reference (like '1993-05-16')
        timeref (str): time reference (string of seconds since midnight)

    Return:
        (datetime.datetime)
    """
    return dt2float(str2dt(dateref) + timedelta(seconds=float(timeref)))


def str2dt(string, *args, **kwargs):
    """Return string converted to datetime"""
    return parse(string, *args, **kwargs)
