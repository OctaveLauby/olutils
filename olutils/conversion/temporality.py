"""Convenient converters for temporality"""
from collections.abc import Iterable
from datetime import datetime, timedelta
from dateutil.parser import parse

# TODO : Handle timezones

DATE_REF = datetime(1970, 1, 1)

HOUR = 3600
DAY = 24 * HOUR
YEAR = 365.25 * DAY

UNIT_TO_SEC = {
    's': 1,
    'sec': 1,
    'second': 1,
    'min': 60,
    'minute': 60,
    'h': HOUR,
    'hour': HOUR,
    'd': DAY,
    'day': DAY,
    'month': YEAR / 12,
    'y': YEAR,
    'year': YEAR,
}


def convert_ts(x, unit):
    """Convert timestamp(s) in secs to given unit from given start

    Args:
        x (float or iterable): timestamp(s)
        unit (str): unit to convert into (min, day, month, year, dt, td)

    Return:
        (float or iterable)
            if x is list, set or tuple, return list set or tuple
            elif x is numpy array and unit is not dt or td, return numpy array
            elif x is another iterable, return map-object
    """
    try:
        divisor = UNIT_TO_SEC[unit]
    except KeyError:
        divisor = None
    try:
        if divisor:
            return x / divisor
        if unit in ["dt", "datetime"]:
            return float2dt(x)
        if unit in ["td", "timedelta"]:
            return timedelta(seconds=float(x))
        raise ValueError("Unknown time unit '%s'" % unit)
    except TypeError:
        if isinstance(x, (list, set, tuple)):
            return type(x)(convert_ts(tick, unit) for tick in x)
        if isinstance(x, Iterable):
            return map(lambda tick: convert_ts(tick, unit), x)
        raise TypeError(f"Can't convert type {type(x)}") from None


def dt2float(dt):
    """Return seconds since the Unix Epoch"""
    return (dt-DATE_REF).total_seconds()


def float2dt(timestamp):
    """Return datetime from seconds since the Unix Epoch"""
    return DATE_REF + timedelta(seconds=float(timestamp))


def str2dt(string, *args, **kwargs):
    """Return string converted to datetime"""
    return parse(string, *args, **kwargs)
