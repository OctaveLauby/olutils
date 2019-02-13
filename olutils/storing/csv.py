from csv import DictReader, DictWriter

from olutils.files import sopen
from olutils.params import read_params
from olutils.tools import countiter


def read_csv(path, delimiter="smart", encoding=None, **params):
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

    with sopen(path, "w+", encoding=params.encoding) as file:
        writer = DictWriter(
            file,
            fieldnames=fieldnames,
            lineterminator="\n",
            delimiter=params.delimiter
        )
        file.write(params.delimiter.join(header) + "\n")
        for row in rows:
            writer.writerow(row)
