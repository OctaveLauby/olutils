"""Functions for object saving and loading."""
import json
import os
import pickle

from olutils.files import sopen
from olutils.params import read_params
from .csv import read_csv, write_csv


# --------------------------------------------------------------------------- #
# Object management


def load(path, mthd=None, encoding=None, **params):
    """Load object at path given a method

    Args:
        path (str)  : path where obj is stored
        mthd (str): method of storing
            csv     > return iterable on rows
                use iter_csv to personalize loading
            json    > return obj using json loading library
            pickle  > return obj using pickle loading method
            None    > catch method from path extension
        encoding (str): file encoding
            None for default
            'utf-8' for classic Linux encoding
            'utf-8-sig' for classic windows encoding
        **params: @see json.load or pickle.load or iter_csv
            iter_csv dft param v changed to False

    Return:
        (object)
    """
    if mthd is None:
        mthd = path.split(".")[-1]

    res = None
    if mthd == "csv":
        res = read_csv(path, encoding=encoding, **params)
    elif mthd == "json":
        with open(path, encoding=encoding) as file:
            res = json.load(file, **params)
    elif mthd == "pickle":
        with open(path, "rb", encoding=encoding) as file:
            res = pickle.load(file, **params)
    else:
        raise ValueError(f"Unknown mthd '{mthd}'")
    return res


def save(obj, path, mthd=None, encoding=None, **params):
    """Save object to path given a method

    Args:
        obj (object): object to store
        path (str)  : path where to save object
        mthd (str): method of storing
            csv     > store as csv file (requires obj to be list of dict)
                use write_csv to personalize saving
            json    > store as pretty json file (requires obj to be json like)
            pickle  > store as pickle file
            None    > catch method from path extension
        encoding (str): file encoding
            None for default
            'utf-8' for classic Linux encoding
            'utf-8-sig' for classic windows encoding
        **params: @see json.dump or pickle.dump or write_csv
            with json, encoding issues can be avoid using ensure_ascii=False
    """
    directory = os.path.dirname(path)

    if mthd is None:
        mthd = path.split(".")[-1]

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if mthd == "csv":
        write_csv(obj, path, encoding=encoding, **params)
    elif mthd == "json":
        with sopen(path, "w", encoding=encoding) as file:
            params = read_params(
                params,
                {'sort_keys': True, 'indent': 4, 'separators': (',', ': ')},
                safe=False,
            )
            json.dump(
                obj, file, **params
            )
    elif mthd == "pickle":
        with sopen(path, "wb", encoding=encoding) as file:
            pickle.dump(obj, file, **params)
    else:
        raise ValueError(f"Unknown mthd '{mthd}'")
