"""Function to manage files"""
import os
import shutil


# --------------------------------------------------------------------------- #
# File / Dir management

def mkdirs(dirtree):
    """Build entire tree of directories if does not exists"""
    if dirtree and not os.path.isdir(dirtree):
        os.makedirs(dirtree)


def rmdirs(dirtree):
    """Remove entire tree of directories

    Same as @see `shutil.rmtree`
    """
    return shutil.rmtree(dirtree)


def sopen(filepath, /, option="w+", **kwargs):
    """Safely open a file, by default for writing, by creating dir tree

    Args:
        filepath (str)
        option (str):
            'r'       open for reading (default)
            'w'       open for writing, truncating the file first
            'a'       open for writing, appending to the end of the file if it exists
            't'       text mode (default)
            '+'       open a disk file for updating (reading and writing)
        **kwargs: @see `open`
    """
    mkdirs(os.path.dirname(filepath))
    return open(filepath, option, **kwargs)
