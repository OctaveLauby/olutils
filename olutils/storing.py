"""Functions for object saving and loading."""
import json
import os
import pickle
from csv import DictReader, DictWriter

from .files import safe_open
from .params import read_params
from .tools import countiter


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
        params['v'] = params.get('v', False)
        res = iter_csv(path, encoding=encoding, **params)
    elif mthd == "json":
        with open(path,  encoding=encoding) as file:
            res = json.load(file, **params)
    elif mthd == "pickle":
        with open(path, "rb",  encoding=encoding) as file:
            res = pickle.load(file, **params)
    else:
        raise ValueError("Unknown mthd '%s'" % mthd)
    return res


def save(obj, path, mthd=None, encoding=None, **params):
    """Save object to path given a method

    Args:
        obj (object): object to store
        path (str)  : path where to save object
        mthd (str): method of storing
            csv     > store as csv file (requires obj to be list of dict)
                use write_csv to personalize saving
            json    > store as json file (requires obj to be json like)
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
        with safe_open(path, "w", encoding=encoding) as file:
            params = read_params(
                params,
                {'sort_keys': True, 'indent': 4, 'separators': (',', ': ')},
                safe=False,
            )
            json.dump(
                obj, file, **params
            )
    elif mthd == "pickle":
        with safe_open(path, "wb", encoding=encoding) as file:
            pickle.dump(obj, file, **params)
    else:
        raise ValueError("Unknown method '%s'" % mthd)


def iter_csv(path, delimiter="smart", encoding=None, **params):
    """Return DictReader iterator on file at path & display row count

    Args:
        path (str)      : path to input
        delimiter (str) : delimiter for columns
            "smart" > try common delimiters and use the one building more cols
        encoding (str)  : encoding of file
        **params (dict) : @see utils.tools.countiter

    Returns:
        (iterator)
    """
    if delimiter == "smart":
        with open(path, encoding=encoding) as file:
            line = file.readline()
        delimiters = sorted([
            (delimiter, len(line.split(delimiter))) for delimiter in ",;\t"
        ], key=lambda i: i[1], reverse=True)
        delimiter, n_cols = delimiters[0]
        if n_cols <= 1:
            raise ValueError("Could not find delimiter of '%s'" % path)

    with open(path, encoding=encoding) as file:
        reader = DictReader(file, delimiter=delimiter)
        countiter(reader, start=1, **params)


def write_csv(rows, path, fieldnames=None, header=None, pretty=False, **params):
    """"Write a list of dictionaries to path

    Args:
        rows (list of dict) : list of rows (dictionaries sharing same keys)
        path (str)          : path to output (path tree is auto-generated)
        fieldnames  (n-list of str) : from rows to use (dft is row keys)
        header      (n-list)        : column names regarding field names
        pretty      (bool)          : pretty frmt header
        params (dict):
            encoding    dft is None
            delimiter   dft is ","
    """
    params = read_params(params, {'delimiter': ",", 'encoding': None})

    if fieldnames is None:
        try:
            fieldnames = list(rows[0].keys())
        except IndexError:
            raise ValueError("Can't write an empty list of dictionaries")

    header = fieldnames if header is None else header
    assert len(header) == len(fieldnames), (
        "Specified header (%s) must have same length as fieldnames (%s)"
        % (len(header), len(fieldnames))
    )
    if pretty:
        header = [
            " ".join(map(str.capitalize, field.split('_')))
            for field in fieldnames
        ]

    with safe_open(path, "w+", encoding=params.encoding) as file:
        writer = DictWriter(
            file,
            fieldnames=fieldnames,
            lineterminator="\n",
            delimiter=params.delimiter
        )
        file.write(params.delimiter.join(header) + "\n")
        for row in rows:
            writer.writerow(row)
