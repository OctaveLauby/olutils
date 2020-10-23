import pytest
from collections import OrderedDict

from olutils.storing import rowreader


def test_RowReader():

    # ---- Simple test
    reader = rowreader.RowReader(
        fields={'field1': "Header1", 'field2': "Header2"},
    )

    row = reader.read({'Header1': 1, 'Header2': 2, 'Header3': 3})
    assert isinstance(row, OrderedDict)
    assert row == {'field1': 1, 'field2': 2}

    with pytest.raises(KeyError):
        reader.read({'Header1': 1, 'Header3': 3})

    # ---- More Elaborate test

    label_func = lambda row: str(row['id']) + "." + row['name']

    reader = rowreader.RowReader(
        fields={'id': "ID", 'name': "Nom"},
        conversions={'id': int},
        operations={'label': label_func},
    )
    row = reader.read({'ID': "8", 'Nom': "Octave"})
    assert row == {'id': 8, 'name': "Octave", 'label': "8.Octave"}

    reader = rowreader.RowReader(
        fields={'id': "ID", 'name': "Nom"},
        conversions={'id': int},
        operations={'label': label_func},
        delete=['name'],
    )
    row = reader.read({'ID': "8", 'Nom': "Octave"})
    assert row == {'id': 8, 'label': "8.Octave"}
