from os.path import exists


def get_next_path(path_frmt: str, start: int = 1) -> str:
    """Return next available path based on path_frmt (1 positional-placeholder)"""
    return path_frmt.format(get_next_path_index(path_frmt, start=start))


def get_next_path_index(path_frmt: str, start: int = 1) -> int:
    """Get next index of given path format (1 positional-placeholder)

    Raises:
        ValueError: if path_frmt does not contain one and only one positional-placeholder
                    such as '{}' or '{:03d}'
    """
    try:
        # Try some random int to check path_frmt consistency
        assert "3823243077" in path_frmt.format(3823243077)
    except (IndexError, AssertionError):
        # IndexError means more than one placeholder, AssertionError means none
        raise ValueError("path_frmt must contain only one positional-placeholder") from None
    except KeyError:
        raise ValueError("path_frmt must contain no named-placeholder") from None

    i = start
    while exists(path_frmt.format(i)):
        i += 1
    return i
