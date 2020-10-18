"""Convenient tools to read and encapsulate rows (dictionaries)"""
from collections import OrderedDict

from olutils.compare import content_diff


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
        super().__init__(content)
        self._attributes = []
        items = content.items() if isinstance(content, dict) else content
        for key, value in items:
            self.setattr(key, value)

    @property
    def attributes(self):
        """Ordered row attributes/keys"""
        return self._attributes

    def delattr(self, key):
        """Remove attribute"""
        try:
            self.pop(key)
        except KeyError:
            raise AttributeError(
                f"Row does not contain attribute '{key}', it can't be deleted"
            ) from None

    def pop(self, key, *args, **kwargs):
        """Remove specified key and return the corresponding value"""
        output = super().pop(key, *args, **kwargs)
        try:
            self._attributes.remove(key)
            delattr(self, key)
        except (ValueError, AttributeError):
            pass
        return output

    def setattr(self, key, value):
        """Set attribute and fills attributes list"""
        if key not in self.attributes:
            self._attributes.append(key)
        self[key] = value
        setattr(self, key, value)


class RowReader:
    """Convenient row reader that includes attr conversions and building"""

    def __init__(self, fields, conversions=None, operations=None, delete=None):
        """Init a row row reader instance

        Args:
            fields (dict)       : (attribute, column name) items to read attr
                from initial row
            conversions (dict)  : (attribute, conversion func) items to convert
                attributes read from rows
            operations (dict)   : (attribute, func) to build new attributes
                from instance built with read and converted attributes
                One should use OrderedDict if operation order matters
            delete (list)       : attributes to delete ones building is over

        Example:
            >> reader = RowReader(
                fields={'id': "ID", 'name': "Name"},
                conversions={'id': int},
                operations={'label': lambda r: str(r.id) + "." + r.name}
            )
            >> row = reader.read({'ID': "8", 'name': "Name"})
            >> assert row.id == 8
            >> assert row.name == "Octave"
            >> assert row.label == "8.Octave"
        """
        self.fields = fields
        self.conversions = conversions if conversions else {}
        self.operations = operations if operations else {}
        self.delete = delete if delete else []

    def read(self, irow):
        """Build an instance from initial row with required attributes

        Args:
            irow (dict): row to read

        Raises:
            (KeyError) if a field is missing in row

        Return:
            (self.rowcls)
        """
        try:
            row = Row(OrderedDict([
                (attr, irow[field])
                for attr, field in self.fields.items()
            ]))
        except KeyError:
            diff = content_diff(irow.keys(), self.fields.values())
            raise KeyError(
                f"Row is missing keys: {', '.join(map(repr, diff['plus']))}"
            ) from None

        for attr, func in self.conversions.items():
            row.setattr(attr, func(getattr(row, attr)))

        for attr, func in self.operations.items():
            row.setattr(attr, func(row))

        for attr in self.delete:
            row.delattr(attr)

        return row
