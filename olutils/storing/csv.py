"""CSV File reading and writing

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
from typing import Iterable, List

from olutils.typing import RowDict
from olutils.os import sopen
from olutils.params import read_params
from olutils.sequencing import countiter
from .common import DFT_EOL


def read_csv(
    path: str,
    /,
    *,
    delimiter: str = "smart",
    mode: str = None,
    encoding: str = None,
    **kwargs,
) -> Iterable[RowDict]:
    """Return csv.DictReader iterator on file at path (can display row count)

    Args:
        path            : path to input
        delimiter       : delimiter for columns
            "smart" > try common delimiters and use the one building more cols
        mode            : mode to open file with (default is 'r')
        encoding        : encoding of file
        **kwargs        : @see `~olutils.countiter`
            vbatch      nb of lines b/w progress displays (dft=0, no display)
            start       first index of progress counter (dft=1)
    """
    mode = "r" if mode is None else mode
    if delimiter == "smart":
        with open(path, mode, encoding=encoding) as file:
            line = file.readline()
        delimiters = sorted(
            [(delimiter, len(line.split(delimiter))) for delimiter in ",;\t"],
            key=lambda i: i[1],
            reverse=True,
        )
        delimiter, n_cols = delimiters[0]
        if n_cols <= 1:
            raise ValueError(f"Could not find delimiter of '{path}'")

    def row_iterator(filepath):
        """Iterate row of file at path"""
        with open(filepath, mode, encoding=encoding) as buffer:
            reader = DictReader(buffer, delimiter=delimiter)
            for elem in countiter(reader, **kwargs):
                yield elem

    kwargs["vbatch"] = kwargs.pop("vbatch", 0)
    kwargs["start"] = kwargs.pop("start", 1)
    return row_iterator(path)


def write_csv(
    rows: Iterable[RowDict],
    path: str,
    /,
    *,
    fieldnames: List[str] = None,
    header: List[str] = None,
    pretty: bool = False,
    encoding: str = None,
    **kwargs,
):
    """ "Write a list of dictionaries to path

    Args:
        rows        : rows (dictionaries sharing same keys)
        path        : path to output (path tree is auto-generated)
        fieldnames  (n-list of str) : from rows to use (dft is row keys)
        header      (n-list)        : column names regarding field names
        pretty      : pretty frmt header
        encoding    : encoding to open output
        **kwargs: @see `csv.DictWriter`
            delimiter       dft is ","
            lineterminator  dft is DFT_EOL
            restval         dft is None if field missing in a row
            extrasaction    dft is "ignore" additional fields in rows

    Raise:
        (ValueError): empty rows and fieldnames is None
        (TypeError) : first row is not a dictionary and fieldnames is None
        else same behavior than csv.DictWriter
    """
    kwargs = read_params(
        kwargs,
        {
            "delimiter": ",",
            "lineterminator": DFT_EOL,
            "restval": None,
            "extrasaction": "ignore",  # Ignore additional keys in rows
        },
        safe=False,
    )
    i_rows = iter(rows)

    # Read fieldnames
    if fieldnames is None:
        try:
            fstrow = next(i_rows)
        except StopIteration:
            raise ValueError("Can't deduce fieldnames if rows is empty") from None
        try:
            fieldnames = list(fstrow.keys())
        except AttributeError:
            raise TypeError("rows must be an iterable on dictionaries") from None

    # Read and compute header
    header = fieldnames if header is None else header
    assert len(header) == len(fieldnames), (
        f"Specified header must have same length as fieldnames"
        f" ({len(header)} != {len(fieldnames)})"
    )
    if pretty:
        header = [
            " ".join(map(str.capitalize, field.split("_"))) for field in fieldnames
        ]

    # Write file
    with sopen(path, "w+", encoding=encoding) as file:
        # TODO : find a convenient way to raise error when field is missing
        writer = DictWriter(file, fieldnames=fieldnames, **kwargs)
        file.write(kwargs["delimiter"].join(header) + kwargs["lineterminator"])
        writer.writerows(rows)
