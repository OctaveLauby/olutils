"""Function to manage files"""
import os
import shutil


# --------------------------------------------------------------------------- #
# File / Dir management


rmtree = shutil.rmtree


def rmdirs(dirtree):
    return rmtree(dirtree)


def safe_open(filepath, option="w+", **params):
    """Safely open a file, by default for writing, by creating dir tree"""
    dirtree = os.path.dirname(filepath)
    if dirtree:
        smart_mkdirs(dirtree)
    return open(filepath, option, **params)


def smart_mkdirs(dirtree):
    """Build """
    if not dirtree:
        return
    if os.path.isdir(dirtree):
        return
    return os.makedirs(dirtree)
