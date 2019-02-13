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
    """Remove entire tree of directories (same as shutil.rmtree)"""
    return shutil.rmtree(dirtree)


def sopen(filepath, option="w+", **params):
    """Safely open a file, by default for writing, by creating dir tree"""
    dirtree = os.path.dirname(filepath)
    mkdirs(dirtree)
    return open(filepath, option, **params)
