"""Error converter(s)"""


def err2str(error, msg_only=False):
    """Return string of error"""
    if msg_only:
        return str(error)
    return f"{error.__class__.__name__} - {str(error)}"
