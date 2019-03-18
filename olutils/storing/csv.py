"""This module provide functions to read and write csv.

It is based on csv library, and add a layer so that :
- Functions open and close file
- delimiter can be automatically guessed for reading
- fieldnames can be deduced from fst row in reading

Also, because it is based on csv library, it has same limitations :
- empty string and None are not distinguished
- delimiter must be single character

@see https://stackoverflow.com/questions/11379300/csv-reader-behavior-with-none-and-empty-string
"""
from csv import DictReader, DictWriter
from itertools import chain

from olutils.files import sopen
from olutils.params import read_params
from olutils.tools import countiter


def read_csv(path, delimiter="smart", encoding=None, **params):
    """Return csv.DictReader iterator on file at path (can display row count)

    Args:
        path (str)      : path to input
        delimiter (str) : delimiter for columns
            "smart" > try common delimiters and use the one building more cols
        encoding (str)  : encoding of file
        **params (dict) : @see utils.tools.countiter
            v_batch     dft value is 0 (no display)

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

    params['v_batch'] = params.pop('v_batch', 0)
    with open(path, encoding=encoding) as file:
        reader = DictReader(file, delimiter=delimiter)
        for elem in countiter(reader, start=1, **params):
            yield elem


def write_csv(rows, path, fieldnames=None, header=None, pretty=False,
              encoding=None, **params):
    """"Write a list of dictionaries to path

    Args:
        rows (iterable of dict) : rows (dictionaries sharing same keys)
        path (str)              : path to output (path tree is auto-generated)
        fieldnames  (n-list of str) : from rows to use (dft is row keys)
        header      (n-list)        : column names regarding field names
        pretty      (bool)          : pretty frmt header
        encoding    (str)           : encoding to open output
        params (dict): @see params for csv.DictWriter
            delimiter       dft is ","
            lineterminator  dft is "\n"
            restval         dft is None if field missing in a row
            extrasaction    dft is "ignore" additional fields in rows

    Raise:
        (ValueError) if rows empty and fieldnames is None
        (TypeError) if fst row is not a dictionary and fieldnames is None
        (---) then same behavior than csv.DictWriter
    """
    encoding = params.pop('encoding', None)
    params = read_params(params, {
        'delimiter': ",",
        'lineterminator': "\n",
        'restval': None,
        'extrasaction': "ignore"  # Ignore additional keys if rows
    }, safe=False)
    i_rows = iter(rows)

    # Read fieldnames
    if fieldnames is None:
        try:
            fstrow = next(i_rows)
        except StopIteration:
            raise ValueError(
                "Can't deduce fieldnames if rows is empty"
            ) from None
        try:
            fieldnames = list(fstrow.keys())
        except AttributeError:
            raise TypeError(
                "rows must be an iterable on dictionaries"
            ) from None
        i_rows = chain([fstrow], i_rows)

    # Read and compute header
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

    # Write file
    with sopen(path, "w+", encoding=encoding) as file:
        # TODO : find a convenient way to raise error when field is missing
        writer = DictWriter(file, fieldnames=fieldnames, **params)
        file.write(params['delimiter'].join(header) + "\n")
        writer.writerows(rows)
