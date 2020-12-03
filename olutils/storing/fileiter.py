from os.path import exists


def get_next_index(path_frmt, start=1):
    """Get next index of given path format

    path_frmt must contains a substring such as '{}' or '{:03d}'
    """
    i = start
    while exists(path_frmt.format(i)):
        i += 1
    return i


def get_next_path(path_frmt, **kwargs):
    """Return next available path based on path format

    path_frmt must contains a substring such as '{}' or '{:03d}'
    """
    return path_frmt.format(get_next_index(path_frmt, **kwargs))
