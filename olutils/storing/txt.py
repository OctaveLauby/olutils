"""This module provide functions to read and write text files."""
import re
from collections.abc import Iterable

from olutils.files import sopen
from .common import DFT_EOL


def rm_eol(line):
    """Return line with end of line removed"""
    return line.rstrip("\n\r")


def read_txt(path, rtype="list", w_eol=True, f_eol=None,
             encoding=None):
    """Return content of text file at path

    Args:
        path (str)      : path to write to
        rtype (str)     : type to return
            "iterable"
            "list"  > list of strings
            "str"   > string
        w_eol (bool)    : return lines with line terminators
        f_eol (str)     : force line terminators to a given string
        iterator (bool) : return iterator on lines

    Return:
        (list)
    """
    # Define function to map lines
    if not w_eol:
        line_conv = lambda line: rm_eol(line)
    elif f_eol is None:
        line_conv = lambda line: line
    elif isinstance(f_eol, str):
        line_conv = lambda line: rm_eol(line) + f_eol
    else:
        raise TypeError(f"f_eol must be str or NoneType, got {type(f_eol)}")

    # Create row iterator
    def line_iterator(path):
        """Iterate lines of file at path"""
        with open(path, encoding=encoding) as file:
            for line in file:
                yield line_conv(line)

    # Return
    line_iter = line_iterator(path)
    if rtype in [list, "list"]:
        return [line_conv(line) for line in line_iter]
    elif rtype in [Iterable, "iter", "iterable"]:
        return line_iter
    elif rtype in [str, "str", "string"]:
        return "".join(line_iter)
    else:
        return ValueError(f"Unexpected value for rtype param: {rtype}")


def write_txt(content, path, has_eol=True, eol=DFT_EOL, encoding=None):
    """Write content in a text file

    Args:
        content (str or Iterable[str]): list of rows or content to write
        path (str)      : path to write to
        has_eol (bool)  : whether lines already have line terminators
            used only if content is an iterator
        eol (str)       : line terminator to use if lines have None
        encoding (str)  : encoding of file
    """
    with sopen(path, "w+", encoding=encoding) as file:
        if isinstance(content, str):
            file.write(content)
        elif isinstance(content, Iterable):
            if not has_eol:
                content = map(lambda line: line + eol, content)
            file.writelines(content)
        else:
            file.write(str(content))