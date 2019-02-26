import pytest

from olutils.storing import csvplus


def test_Row():

    row = csvplus.Row([
        ('field3', 3),
        ('field1', 1),
        ('field2', 2),
    ])
    assert row == {'field1': 1, 'field2': 2, 'field3': 3}
    assert row.attributes == ['field3', 'field1', 'field2']
    assert row.field1 == 1
    assert row.field2 == 2
    assert row.field3 == 3


def test_RowReader():

    # ---- Simple test
    reader = csvplus.RowReader(
        attrfields={'field1': "Header1", 'field2': "Header2"},
    )

    row = reader.read({'Header1': 1, 'Header2': 2, 'Header3': 3})
    assert isinstance(row, csvplus.Row)
    assert row == {'field1': 1, 'field2': 2}
    assert row.attributes == ['field1', 'field2']

    with pytest.raises(csvplus.RowUncomplete):
        row = reader.read({'Header1': 1, 'Header3': 3})

    # ---- More Elaborate test

    reader = csvplus.RowReader(
        attrfields={'id': "ID", 'name': "Nom"},
        attrconvert={'id': int},
        attroperation={'label': lambda row: str(row.id) + "." + row.name}
    )
    row = reader.read({'ID': "8", 'Nom': "Octave"})
    assert row == {'id': 8, 'name': "Octave", 'label': "8.Octave"}
    assert row.attributes == ['id', 'name', 'label']
