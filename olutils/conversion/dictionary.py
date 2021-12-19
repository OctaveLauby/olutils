"""Dictionary converters"""
from typing import Any, Callable, Dict, Hashable

from olutils.collection.functions import identity


def basedict(__obj: Dict, /, leafconv: Callable = identity) -> Dict:
    """Return base dict from object (recursive)

    Args:
        __obj (dict-like): dict-like object to recursively convert
            for instance OrderedDict or defaultdict
        leafconv: function to convert leaves (not dict values)
    """
    return {
        key: basedict(value, leafconv=leafconv)
        if isinstance(value, dict)
        else leafconv(value)
        for key, value in __obj.items()
    }


def dict2str(
    __obj: Any,
    /,
    *,
    bullets: str = "#*>-",
    indent: str = "\t",
    prefix: str = "",
    keyconv: Callable[[Hashable], str] = str,
    leafconv: Callable[[Any], str] = str,
) -> str:
    """Convert dict to pretty formatted string

    Args:
        __obj    : dictionary to format to string
        bullets     : list of bullets to use for dict-ladders
        indent      : indent to add when going to next dict-ladder
        prefix      : prefix before each row in string
        keyconv     : dict-key string converter
        leafconv    : dict-leaf string converter

    Returns:
        (str) pretty representation of __obj
    """
    if not isinstance(__obj, dict):
        return leafconv(__obj)

    bullet = bullets[0] if bullets else ""
    exbullet = "" if bullet in ["", " "] else (bullet + " ")
    nbullets = bullets[1:] if bullets else ""

    string = ""
    try:
        key_maxsize = max(len(keyconv(key)) for key in __obj.keys())
    except ValueError:
        return "<empty dict>"
    for key, value in __obj.items():
        if string:
            string += "\n"
        if isinstance(value, dict):
            string += prefix + exbullet + keyconv(key).ljust(key_maxsize) + ":"
            value_str = dict2str(
                value,
                bullets=nbullets,
                indent=indent,
                prefix=prefix + indent,
                leafconv=leafconv,
                keyconv=keyconv,
            )
            if value:
                string += "\n" + value_str
            else:
                string += " " + value_str
        else:
            string += (
                prefix
                + exbullet
                + keyconv(key).ljust(key_maxsize)
                + ": "
                + leafconv(value)
            )
    return string
