"""Convenient tools to read and encapsule rows (dictionaries)"""
from collections import OrderedDict


class RowUncomplete(Exception):
    pass


class Row(OrderedDict):
    """Extension of OrderedDict with items accessible through attributes"""

    def __init__(self, content):
        """Init Row with content

        Args:
            content (dict or list): content of row

        Example:
            >> row = Row([('key1': 1), ('key0', 0)])
            >> row.setattr('key2': 2)
            >> assert row.key0 == 0
            >> assert row.key1 == 1
            >> assert row.key2 == 2
            >> assert row.attributes == ['key1', 'key0', 'key2']
        """
        self._attributes = []
        items = content.items() if isinstance(content, dict) else content
        for key, value in items:
            self.setattr(key, value)

    @property
    def attributes(self):
        """Ordered row attributes/keys"""
        return self._attributes

    def setattr(self, key, value):
        """Set attribute and fills attributes list"""
        if key not in self.attributes:
            self._attributes.append(key)
        self[key] = value
        setattr(self, key, value)


class RowReader(object):
    """Convenient row reader that includes attr conversions and building"""

    def __init__(self, attrfields, attrconvert=None, attroperation=None):
        """Init a row row reader instance

        Args:
            attrfields (dict)   : (attribute, column name) items to read attr
                from initial row
            attrconvert (dict)  : (attribute, conversion func) items to convert
                attributes read from rows
            attroperation (dict): (attribute, func) to build new attributes
                from instance built with read and converted attributes
                One should use OrderedDict if operation order matters

        Example:
            >> reader = RowReader(
                attrfields={'id': "ID", 'name': "Name"},
                attrconvert={'id': int},
                attroperation={'label': lambda r: str(r.id) + "." + r.name}
            )
            >> row = reader.read({'ID': "8", 'name': "Name"})
            >> assert row.id == 8
            >> assert row.name == "Octave"
            >> assert row.label == "8.Octave"
        """
        self.attrfields = attrfields
        self.attrconvert = attrconvert if attrconvert else {}
        self.attroperation = attroperation if attroperation else {}

    def read(self, irow):
        """Build an instance from initial row with required attributes

        Args:
            irow (dict): row to read

        Raises:
            (RowUncomplete) if a field is missing in row

        Return:
            (self.rowcls)
        """
        try:
            row = Row(OrderedDict([
                (attr, irow[field])
                for attr, field in self.attrfields.items()
            ]))
        except KeyError:
            raise RowUncomplete(
                "row fields %s does not contain all expected fields %s"
                % (list(irow.keys()), list(self.attrfields.values()))
            )

        for attr, func in self.attrconvert.items():
            row.setattr(attr, func(getattr(row, attr)))

        for attr, func in self.attroperation.items():
            row.setattr(attr, func(row))

        return row
