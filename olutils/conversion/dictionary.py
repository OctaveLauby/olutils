"""Conversion functions for dictionaries"""


def basedict(obj, leaf_conv=lambda x: x):
    """Return base dict from dict-like object (recursive)

    Args:
        obj (dict-like)     : object to recursively convert
        leaf_conv (callable): function to convert leafs (not dict values)

    Return:
        (dict)
    """
    if isinstance(obj, dict):
        return {
            key: basedict(value, leaf_conv=leaf_conv)
            for key, value in obj.items()
        }
    return leaf_conv(obj)


def dict2str(obj, bullets="#*>-", indent="\t", prefix="",
             keyconv=str, leafconv=str):
    """Convert dict to pretty formatted string

    Args:
        obj (dict)      : dictionary to format to string
        bullets (str)   : list of bullets to use for dict-ladders
        indent (str)    : indent to add when going to next dict-ladder
        prefix (str)    : prefix before each row in string
        keyconv (func)  : dict-key string converter
        leafconv (func) : dict-leaf string converter

    Return:
        (str) pretty representation of obj
    """
    if not isinstance(obj, dict):
        return leafconv(obj)

    bullet = bullets[0] if bullets else ""
    exbullet = "" if bullet in ["", " "] else (bullet + " ")
    nbullets = bullets[1:] if bullets else ""

    string = ""
    try:
        key_maxsize = max(len(keyconv(key)) for key in obj.keys())
    except ValueError:
        return "<empty dict>"
    for key, value in obj.items():
        if string:
            string += "\n"
        if isinstance(value, dict):
            string += prefix + exbullet + keyconv(key).ljust(key_maxsize) + ":"
            value_str = dict2str(
                value, bullets=nbullets, indent=indent, prefix=prefix+indent,
                leafconv=leafconv, keyconv=keyconv
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
