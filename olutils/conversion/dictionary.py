"""Dictionary converters"""
from olutils.collection.functions import identity


def basedict(__object, /, leafconv=identity):
    """Return base dict from object (recursive)

    Args:
        __object (dict)     : dict-like object to recursively convert
        leafconv (callable) : function to convert leaves (not dict values)

    Return:
        (dict)
    """
    if isinstance(__object, dict):
        return {
            key: basedict(value, leafconv=leafconv)
            for key, value in __object.items()
        }
    return leafconv(__object)


def dict2str(__object, /, *, bullets="#*>-", indent="\t", prefix="",
             keyconv=str, leafconv=str):
    """Convert dict to pretty formatted string

    Args:
        __object (dict) : dictionary to format to string
        bullets (str)   : list of bullets to use for dict-ladders
        indent (str)    : indent to add when going to next dict-ladder
        prefix (str)    : prefix before each row in string
        keyconv (func)  : dict-key string converter
        leafconv (func) : dict-leaf string converter

    Return:
        (str) pretty representation of __object
    """
    if not isinstance(__object, dict):
        return leafconv(__object)

    bullet = bullets[0] if bullets else ""
    exbullet = "" if bullet in ["", " "] else (bullet + " ")
    nbullets = bullets[1:] if bullets else ""

    string = ""
    try:
        key_maxsize = max(len(keyconv(key)) for key in __object.keys())
    except ValueError:
        return "<empty dict>"
    for key, value in __object.items():
        if string:
            string += "\n"
        if isinstance(value, dict):
            string += prefix + exbullet + keyconv(key).ljust(key_maxsize) + ":"
            value_str = dict2str(
                value,
                bullets=nbullets,
                indent=indent,
                prefix=prefix+indent,
                leafconv=leafconv,
                keyconv=keyconv,
            )
            if value:
                string += "\n" + value_str
            else:
                string += " " + value_str
        else:
            string += (
                prefix + exbullet
                + keyconv(key).ljust(key_maxsize)
                + ": " + leafconv(value)
            )
    return string
