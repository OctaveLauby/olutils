"""Temporality converters"""
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


def secs2unit(secs, /, unit):
    """Convert number of seconds to given unit

    Args:
        secs (int|float|iterable): number of seconds
        unit (str): unit to convert to

    Available units:
        s, sec, second      -> second
        min, minute         -> minute
        h, hour             -> hour
        d, day              -> day
        month               -> month
        y, year             -> year
        dt, datetime        -> datetime (secs is interpreted as unix-timestamp)
        td, timedelta       -> timedelta

    Raise:
        (TypeError) : secs-type not handled
        (ValueError): unit not handled

    Return:
        (object)
            if secs is int|float
                if unit is dt: return datetime
                elif unit is timedelta: return timedelta
                else: return int|float
            elif secs is iterable
                if secs is list|set|tuple: return list|set|tuple
                elif secs is ndarray & unit is not dt|td: return ndarray
                else: return map-object
    """
    try:
        divisor = UNIT_TO_SEC[unit]
    except KeyError:
        divisor = None
    try:
        if divisor:
            return secs / divisor
        if unit in ["dt", "datetime"]:
            return ts2dt(secs)
        if unit in ["td", "timedelta"]:
            return timedelta(seconds=float(secs))
        raise ValueError("Unknown time unit '%s'" % unit)
    except TypeError:
        if isinstance(secs, (list, set, tuple)):
            return type(secs)(secs2unit(tick, unit) for tick in secs)
        if not isinstance(secs, str) and isinstance(secs, Iterable):
            return map(lambda tick: secs2unit(tick, unit), secs)
        raise TypeError(f"Can't convert type {type(secs)}") from None


def dt2ts(dt, /):
    """Return seconds since the Unix Epoch"""
    return (dt-DATE_REF).total_seconds()


def ts2dt(ts, /):
    """Return datetime from seconds since the Unix Epoch"""
    return DATE_REF + timedelta(seconds=float(ts))


def str2dt(timestr, /, *args, **kwargs):
    """Return datetime from string

    Args:
        timestr (str)   : string describing a datetime
        *args, **kwargs : @see `dateutil.parser.parse`
    """
    return parse(timestr, *args, **kwargs)
