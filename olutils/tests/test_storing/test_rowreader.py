import pytest

from olutils.storing import rowreader


def test_Row():

    row = rowreader.Row([
        ('field3', 3),
        ('field1', 1),
        ('field2', 2),
    ])
    assert row == {'field1': 1, 'field2': 2, 'field3': 3}
    assert row.attributes == ['field3', 'field1', 'field2']
    assert row.field1 == 1
    assert row.field2 == 2
    assert row.field3 == 3

    row.delattr('field1')
    assert row == {'field2': 2, 'field3': 3}
    assert row.attributes == ['field3', 'field2']
    assert row.field2 == 2
    assert row.field3 == 3
    with pytest.raises(AttributeError):
        row.field1

    assert row.pop('field1', None) is None
    assert row.pop('field2') == 2
    assert row == {'field3': 3}
    assert row.attributes == ['field3']
    assert row.field3 == 3
    with pytest.raises(AttributeError):
        row.field1

    with pytest.raises(KeyError):
        row.pop('field2')
    with pytest.raises(AttributeError):
        row.delattr('field2')


def test_RowReader():

    # ---- Simple test
    reader = rowreader.RowReader(
        fields={'field1': "Header1", 'field2': "Header2"},
    )

    row = reader.read({'Header1': 1, 'Header2': 2, 'Header3': 3})
    assert isinstance(row, rowreader.Row)
    assert row == {'field1': 1, 'field2': 2}
    assert row.attributes == ['field1', 'field2']

    with pytest.raises(KeyError):
        row = reader.read({'Header1': 1, 'Header3': 3})

    # ---- More Elaborate test

    reader = rowreader.RowReader(
        fields={'id': "ID", 'name': "Nom"},
        conversions={'id': int},
        operations={'label': lambda row: str(row.id) + "." + row.name},
    )
    row = reader.read({'ID': "8", 'Nom': "Octave"})
    assert row == {'id': 8, 'name': "Octave", 'label': "8.Octave"}
    assert row.attributes == ['id', 'name', 'label']

    reader = rowreader.RowReader(
        fields={'id': "ID", 'name': "Nom"},
        conversions={'id': int},
        operations={'label': lambda row: str(row.id) + "." + row.name},
        delete=['name'],
    )
    row = reader.read({'ID': "8", 'Nom': "Octave"})
    assert row == {'id': 8, 'label': "8.Octave"}
    assert row.attributes == ['id', 'label']
