"""Functions to read and write text files."""
from collections.abc import Iterable as IterableABC
from typing import Iterable, List, Union

from olutils.collection import identity
from olutils.os import sopen
from .common import DFT_EOL


def rm_eol(line, /):
    """Return line with end of line removed"""
    return line.rstrip("\n\r")


def read_txt(
    path: str,
    /,
    *,
    rtype: type = list,
    w_eol: bool = True,
    f_eol: str = None,
    mode: str = None,
    encoding: str = None,
) -> Union[List[str], str, Iterable[str]]:
    """Return content of text file at path

    Args:
        path    : path to write to
        rtype   : type to return
            Iterable, "iter", "iterable"        -> Iterable on rows
            list, "list"                        -> list of strings
            str, "str", "string"                -> rows joined with ''
        w_eol   : return lines with line terminators
        f_eol   : force line terminators to a given string
        mode    : mode to open file with (default is 'r')
        encoding: encoding used to read file

    Raise:
        (TypeError) : f_eol-type not handled
        (ValueError): rtype not handled
    """
    mode = "r" if mode is None else mode

    # Define function to map lines
    if not w_eol:
        line_conv = rm_eol
    elif f_eol is None:
        line_conv = identity
    elif isinstance(f_eol, str):
        def line_conv(line):
            return rm_eol(line) + f_eol
    else:
        raise TypeError(f"f_eol must be str or NoneType, got {type(f_eol)}")

    # Create row iterator
    def line_iterator() -> Iterable[str]:
        """Iterate lines of file at path"""
        with open(path, mode, encoding=encoding) as file:
            for line in file:
                yield line_conv(line)

    # Return
    line_iter = line_iterator()
    if rtype in [list, "list"]:
        return [line_conv(line) for line in line_iter]
    if rtype in [Iterable, "iter", "iterable"]:
        return line_iter
    if rtype in [str, "str", "string"]:
        return "".join(line_iter)
    raise ValueError(f"Unexpected value for rtype param: {rtype}")


def write_txt(
    content: Union[str, Iterable[str]],
    path: str,
    /,
    *,
    has_eol: bool = True,
    eol: str = DFT_EOL,
    encoding: str = None,
):
    """Write content in a text file

    Args:
        content : list of rows or content to write
        path    : path to write to
        has_eol : whether lines already have line terminators
            used only if content is an iterator
        eol     : line terminator to use if lines have None
        encoding: encoding of file
    """
    with sopen(path, "w+", encoding=encoding) as file:
        if isinstance(content, str):
            file.write(content)
        elif isinstance(content, IterableABC):
            if not has_eol:
                content = map(lambda line: line + eol, content)
            file.writelines(content)
        else:
            file.write(str(content))
