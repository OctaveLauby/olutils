"""Error converters"""


def err2str(error: Exception, /, *, msg_only: bool = False) -> str:
    """Return string of error"""
    if msg_only:
        return str(error)
    return f"{error.__class__.__name__} - {str(error)}"
