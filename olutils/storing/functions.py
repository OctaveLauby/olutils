"""Functions for object saving and loading."""
import json
import os
import pickle

from olutils.files import sopen
from olutils.params import read_params
from .csv import read_csv, write_csv
from .txt import read_txt, write_txt


# --------------------------------------------------------------------------- #
# Object management


def load(path, mthd=None, mode=None, encoding=None, **params):
    """Load object at path given a method

    Args:
        path (str)  : path where obj is stored
        mthd (str): method of storing
            None        > catch method from path extension
            'csv'       > return iterable on rows
            'json'      > return obj using json loading library
            'pickle'    > return obj using pickle loading method
            'txt'       > return content of text file
        mode (str)    : mode to open file with
            default is 'r', except for pickle method where it is 'rb'
        encoding (str): file encoding
            None for default
            'utf-8' for classic Linux encoding
            'utf-8-sig' for classic windows encoding
        **params: available params depend on mthd value
            'csv'       > @see read_csv
                delimiter, ...
            'json'      > @see json.load
            'pickle'    > @see pickle.load
            'txt'       > @see write_txt
                rtype, w_eol, f_eol
    Return:
        (object)
    """
    if mthd is None:
        mthd = path.split(".")[-1]

    res = None
    if mthd == "csv":
        res = read_csv(path, mode=mode, encoding=encoding, **params)
    elif mthd == "json":
        mode = 'r' if mode is None else mode
        with open(path, mode, encoding=encoding) as file:
            res = json.load(file, **params)
    elif mthd == "pickle":
        mode = 'rb' if mode is None else mode
        with open(path, mode, encoding=encoding) as file:
            res = pickle.load(file, **params)
    elif mthd == "txt":
        res = read_txt(path, mode=mode, encoding=encoding, **params)
    else:
        raise ValueError(f"Unknown mthd '{mthd}'")
    return res


def save(obj, path, mthd=None, encoding=None, **params):
    """Save object to path given a method

    Args:
        obj (object): object to store
        path (str)  : path where to save object
        mthd (str): method of storing
            None        > catch method from path extension
            'csv'       > store as csv file (requires obj to be list of dict)
            'json'      > store as pretty json file (requires obj to be json like)
            'pickle'    > store as pickle file
            'txt'       > store as text file
        encoding (str): file encoding
            None for default
            'utf-8' for classic Linux encoding
            'utf-8-sig' for classic windows encoding
        **params: available params depend on mthd value
            'csv'       > @see write_csv
                fieldnames, header, pretty, ...
            'json'      > @see json.dump
                encoding issues can be avoid using ensure_ascii=False
            'pickle'    > @see pickle.dump
            'txt'       > @see write_txt
                has_eol, eol
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
    elif mthd == "txt":
        write_txt(obj, path, encoding=encoding, **params)
    else:
        raise ValueError(f"Unknown mthd '{mthd}'")
